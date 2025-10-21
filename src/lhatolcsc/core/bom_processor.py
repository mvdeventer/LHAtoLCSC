"""
BOM Processor module.

Handles loading, parsing, and validating Excel BOM files.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
from openpyxl import load_workbook

from lhatolcsc.api.models import BOMItem


logger = logging.getLogger(__name__)


class BOMProcessor:
    """
    BOM file processor for Excel files.
    """
    
    COMMON_PART_NAME_COLUMNS = [
        "stock part name",
        "part name",
        "part",
        "component",
        "description",
        "item",
        "mpn",
        "manufacturer part number"
    ]
    
    COMMON_QUANTITY_COLUMNS = [
        "quantity",
        "qty",
        "count",
        "amount"
    ]
    
    COMMON_REFERENCE_COLUMNS = [
        "reference designator",
        "reference",
        "ref",
        "designator",
        "refs"
    ]
    
    def __init__(self):
        """Initialize BOM processor."""
        self.bom_df: Optional[pd.DataFrame] = None
        self.file_path: Optional[Path] = None
        self.column_mapping: Dict[str, str] = {}
    
    def load_bom(self, file_path: str) -> Tuple[bool, str]:
        """
        Load BOM from Excel file.
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            Tuple of (success, message)
        """
        try:
            self.file_path = Path(file_path)
            
            if not self.file_path.exists():
                return False, "File does not exist"
            
            # Try reading with pandas
            if self.file_path.suffix.lower() == '.xlsx':
                self.bom_df = pd.read_excel(file_path, engine='openpyxl')
            elif self.file_path.suffix.lower() == '.xls':
                self.bom_df = pd.read_excel(file_path, engine='xlrd')
            elif self.file_path.suffix.lower() == '.csv':
                self.bom_df = pd.read_csv(file_path)
            else:
                return False, f"Unsupported file format: {self.file_path.suffix}"
            
            logger.info(f"Loaded BOM with {len(self.bom_df)} rows and {len(self.bom_df.columns)} columns")
            
            # Auto-detect columns
            self._auto_detect_columns()
            
            return True, f"Successfully loaded {len(self.bom_df)} items"
            
        except Exception as e:
            logger.error(f"Failed to load BOM: {e}")
            return False, f"Error loading file: {str(e)}"
    
    def _auto_detect_columns(self) -> None:
        """Auto-detect column mappings from BOM file."""
        if self.bom_df is None:
            return
        
        # Normalize column names for comparison
        columns_lower = {col: col.lower().strip() for col in self.bom_df.columns}
        
        # Detect part name column
        for col, col_lower in columns_lower.items():
            if any(name in col_lower for name in self.COMMON_PART_NAME_COLUMNS):
                self.column_mapping['part_name'] = col
                logger.info(f"Auto-detected part name column: {col}")
                break
        
        # Detect quantity column
        for col, col_lower in columns_lower.items():
            if any(name in col_lower for name in self.COMMON_QUANTITY_COLUMNS):
                self.column_mapping['quantity'] = col
                logger.info(f"Auto-detected quantity column: {col}")
                break
        
        # Detect reference designator column
        for col, col_lower in columns_lower.items():
            if any(name in col_lower for name in self.COMMON_REFERENCE_COLUMNS):
                self.column_mapping['reference'] = col
                logger.info(f"Auto-detected reference column: {col}")
                break
    
    def get_columns(self) -> List[str]:
        """
        Get list of column names from BOM.
        
        Returns:
            List of column names
        """
        if self.bom_df is None:
            return []
        return list(self.bom_df.columns)
    
    def set_column_mapping(self, mapping: Dict[str, str]) -> None:
        """
        Set column mapping manually.
        
        Args:
            mapping: Dictionary mapping logical names to actual column names
        """
        self.column_mapping.update(mapping)
        logger.info(f"Column mapping updated: {self.column_mapping}")
    
    def get_bom_items(self) -> List[BOMItem]:
        """
        Extract BOM items from loaded DataFrame.
        
        Returns:
            List of BOMItem objects
        """
        if self.bom_df is None:
            return []
        
        items = []
        part_name_col = self.column_mapping.get('part_name')
        quantity_col = self.column_mapping.get('quantity')
        reference_col = self.column_mapping.get('reference')
        
        if not part_name_col:
            logger.warning("Part name column not mapped")
            return []
        
        for idx, row in self.bom_df.iterrows():
            # Skip empty rows
            if pd.isna(row.get(part_name_col)):
                continue
            
            item = BOMItem(
                row_index=int(idx),
                stock_part_name=str(row[part_name_col]).strip(),
                quantity=int(row[quantity_col]) if quantity_col and not pd.isna(row.get(quantity_col)) else 1,
                reference_designator=str(row[reference_col]).strip() if reference_col and not pd.isna(row.get(reference_col)) else "",
            )
            items.append(item)
        
        logger.info(f"Extracted {len(items)} BOM items")
        return items
    
    def export_bom(self, items: List[BOMItem], output_path: str) -> Tuple[bool, str]:
        """
        Export enhanced BOM to Excel file.
        
        Args:
            items: List of BOMItem objects with LCSC data
            output_path: Path for output file
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Create DataFrame from items
            data = []
            for item in items:
                row = {
                    'Stock Part Name': item.stock_part_name,
                    'Quantity': item.quantity,
                    'Reference Designator': item.reference_designator,
                    'Description': item.description,
                    'Manufacturer': item.manufacturer,
                    'MPN': item.mpn,
                    'LCSC Part Number': item.lcsc_part_number,
                    'Match Confidence': f"{item.match_confidence:.1f}%",
                    'Notes': item.notes
                }
                data.append(row)
            
            df = pd.DataFrame(data)
            
            # Export to Excel
            df.to_excel(output_path, index=False, engine='openpyxl')
            
            logger.info(f"Exported BOM to {output_path}")
            return True, f"Successfully exported to {output_path}"
            
        except Exception as e:
            logger.error(f"Failed to export BOM: {e}")
            return False, f"Error exporting file: {str(e)}"
    
    def validate_bom(self) -> Tuple[bool, List[str]]:
        """
        Validate loaded BOM structure.
        
        Returns:
            Tuple of (is_valid, list of validation messages)
        """
        messages = []
        
        if self.bom_df is None:
            return False, ["No BOM loaded"]
        
        if len(self.bom_df) == 0:
            messages.append("BOM is empty")
        
        if not self.column_mapping.get('part_name'):
            messages.append("Part name column not identified")
        
        # Check for duplicate entries
        if self.column_mapping.get('part_name'):
            duplicates = self.bom_df[self.column_mapping['part_name']].duplicated().sum()
            if duplicates > 0:
                messages.append(f"Warning: {duplicates} duplicate part names found")
        
        is_valid = len(messages) == 0 or all("Warning" in msg for msg in messages)
        return is_valid, messages
