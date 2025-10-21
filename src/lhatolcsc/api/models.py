"""
LCSC API Data Models.

Dataclasses representing API response structures.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class PriceTier:
    """Price tier information."""
    
    quantity: int
    unit_price: float
    currency: str = "USD"
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PriceTier":
        """Create PriceTier from API response dict."""
        return cls(
            quantity=int(data.get("startAmount", data.get("startNumber", 0))),
            unit_price=float(data.get("productPrice", 0.0)),
            currency=data.get("currency", "USD")
        )


@dataclass
class LCSCProduct:
    """LCSC Product information."""
    
    product_number: str  # LCSC part number (e.g., C2653)
    product_code: str
    product_name: str
    manufacturer: str = ""
    manufacturer_part: str = ""  # MPN
    description: str = ""
    category_id: int = 0
    category_name: str = ""
    stock: int = 0
    price_tiers: List[PriceTier] = field(default_factory=list)
    datasheet_url: str = ""
    image_url: str = ""
    is_available: bool = False
    is_pre_sale: bool = False
    package_type: str = ""
    
    @property
    def unit_price(self) -> float:
        """Get the lowest unit price."""
        if not self.price_tiers:
            return 0.0
        return min(tier.unit_price for tier in self.price_tiers)
    
    @property
    def in_stock(self) -> bool:
        """Check if product is in stock."""
        return self.stock > 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LCSCProduct":
        """Create LCSCProduct from API response dict."""
        # Parse price tiers
        price_tiers = []
        if "productPriceList" in data:
            price_tiers = [
                PriceTier.from_dict(p) for p in data["productPriceList"]
            ]
        
        return cls(
            product_number=data.get("productCode", ""),
            product_code=data.get("productCode", ""),
            product_name=data.get("productModel", ""),
            manufacturer=data.get("brandNameEn", data.get("brandName", "")),
            manufacturer_part=data.get("productModel", ""),
            description=data.get("productIntroEn", data.get("productName", "")),
            category_id=int(data.get("parentCatalogId", 0)),
            category_name=data.get("parentCatalogName", ""),
            stock=int(data.get("stockNumber", 0)),
            price_tiers=price_tiers,
            datasheet_url=data.get("pdfUrl", ""),
            image_url=data.get("productImages", ""),
            is_available=bool(data.get("isStock") or int(data.get("stockNumber", 0)) > 0),
            is_pre_sale=bool(data.get("isPresale", False)),
            package_type=data.get("encapStandard", data.get("packageType", ""))
        )


@dataclass
class SearchResult:
    """Search result container."""
    
    products: List[LCSCProduct]
    total: int
    current_page: int
    page_size: int
    
    @property
    def total_pages(self) -> int:
        """Calculate total number of pages."""
        if self.page_size == 0:
            return 0
        return (self.total + self.page_size - 1) // self.page_size
    
    @property
    def has_more(self) -> bool:
        """Check if there are more pages."""
        return self.current_page < self.total_pages


@dataclass
class BOMItem:
    """BOM item representation."""
    
    row_index: int
    stock_part_name: str
    quantity: int = 1
    reference_designator: str = ""
    description: str = ""
    manufacturer: str = ""
    mpn: str = ""
    lcsc_part_number: str = ""
    match_confidence: float = 0.0
    notes: str = ""


@dataclass
class MatchResult:
    """Match result for BOM item."""
    
    bom_item: BOMItem
    lcsc_product: Optional[LCSCProduct] = None
    match_score: float = 0.0
    match_method: str = "none"  # "exact", "fuzzy", "manual", "none"
    alternatives: List[LCSCProduct] = field(default_factory=list)
    matched_at: Optional[datetime] = None
    
    @property
    def is_matched(self) -> bool:
        """Check if item has been matched."""
        return self.lcsc_product is not None
    
    @property
    def confidence_level(self) -> str:
        """Get confidence level description."""
        if self.match_score >= 90:
            return "High"
        elif self.match_score >= 70:
            return "Medium"
        elif self.match_score > 0:
            return "Low"
        return "None"
