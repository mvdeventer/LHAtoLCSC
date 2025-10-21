"""
Fuzzy matching engine for component search.
"""

import logging
from typing import List, Optional, Tuple

from rapidfuzz import fuzz, process

from lhatolcsc.api.client import LCSCClient
from lhatolcsc.api.models import BOMItem, LCSCProduct, MatchResult


logger = logging.getLogger(__name__)


class ComponentMatcher:
    """
    Fuzzy matching engine for BOM components to LCSC parts.
    """
    
    def __init__(self, api_client: LCSCClient, confidence_threshold: int = 75):
        """
        Initialize matcher.
        
        Args:
            api_client: LCSC API client
            confidence_threshold: Minimum confidence score (0-100)
        """
        self.api_client = api_client
        self.confidence_threshold = confidence_threshold
        self.cache: dict = {}
    
    def match_item(
        self,
        bom_item: BOMItem,
        max_alternatives: int = 5
    ) -> MatchResult:
        """
        Find best match for a BOM item.
        
        Args:
            bom_item: BOM item to match
            max_alternatives: Maximum number of alternative matches
            
        Returns:
            MatchResult with best match and alternatives
        """
        logger.info(f"Matching item: {bom_item.stock_part_name}")
        
        # Check cache first
        cache_key = bom_item.stock_part_name.lower().strip()
        if cache_key in self.cache:
            logger.debug(f"Cache hit for: {cache_key}")
            return self.cache[cache_key]
        
        try:
            # Search LCSC API with fuzzy matching
            search_result = self.api_client.search_products(
                keyword=bom_item.stock_part_name,
                match_type="fuzzy",
                page_size=max_alternatives + 5
            )
            
            if not search_result.products:
                logger.warning(f"No matches found for: {bom_item.stock_part_name}")
                result = MatchResult(
                    bom_item=bom_item,
                    match_score=0.0,
                    match_method="none"
                )
                self.cache[cache_key] = result
                return result
            
            # Calculate fuzzy match scores
            scored_products = self._score_products(
                bom_item.stock_part_name,
                search_result.products
            )
            
            # Get best match
            best_product, best_score = scored_products[0]
            
            # Get alternatives
            alternatives = [p for p, s in scored_products[1:max_alternatives]]
            
            # Determine match method
            match_method = "exact" if best_score == 100 else "fuzzy"
            
            result = MatchResult(
                bom_item=bom_item,
                lcsc_product=best_product if best_score >= self.confidence_threshold else None,
                match_score=best_score,
                match_method=match_method if best_score >= self.confidence_threshold else "none",
                alternatives=alternatives
            )
            
            # Update BOM item if matched
            if result.is_matched:
                bom_item.lcsc_part_number = best_product.product_number
                bom_item.manufacturer = best_product.manufacturer
                bom_item.mpn = best_product.manufacturer_part
                bom_item.description = best_product.description
                bom_item.match_confidence = best_score
            
            self.cache[cache_key] = result
            logger.info(f"Match score: {best_score:.1f}% for {bom_item.stock_part_name}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error matching item: {e}")
            result = MatchResult(
                bom_item=bom_item,
                match_score=0.0,
                match_method="error"
            )
            result.bom_item.notes = f"Error: {str(e)}"
            return result
    
    def _score_products(
        self,
        search_term: str,
        products: List[LCSCProduct]
    ) -> List[Tuple[LCSCProduct, float]]:
        """
        Score and rank products by similarity to search term.
        
        Args:
            search_term: Original search term
            products: List of LCSC products
            
        Returns:
            List of (product, score) tuples sorted by score descending
        """
        scored = []
        
        for product in products:
            # Calculate scores for different fields
            name_score = fuzz.ratio(search_term.lower(), product.product_name.lower())
            mpn_score = fuzz.ratio(search_term.lower(), product.manufacturer_part.lower())
            desc_score = fuzz.partial_ratio(search_term.lower(), product.description.lower())
            
            # Weighted average (name and MPN weighted higher)
            score = (name_score * 0.5) + (mpn_score * 0.4) + (desc_score * 0.1)
            
            scored.append((product, score))
        
        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)
        
        return scored
    
    def batch_match(
        self,
        bom_items: List[BOMItem],
        progress_callback: Optional[callable] = None
    ) -> List[MatchResult]:
        """
        Match multiple BOM items in batch.
        
        Args:
            bom_items: List of BOM items to match
            progress_callback: Optional callback for progress updates
            
        Returns:
            List of MatchResult objects
        """
        results = []
        total = len(bom_items)
        
        logger.info(f"Starting batch match for {total} items")
        
        for i, item in enumerate(bom_items):
            result = self.match_item(item)
            results.append(result)
            
            if progress_callback:
                progress_callback(i + 1, total, item.stock_part_name)
        
        logger.info(f"Batch match completed: {total} items processed")
        return results
    
    def clear_cache(self) -> None:
        """Clear the match cache."""
        self.cache.clear()
        logger.info("Match cache cleared")
