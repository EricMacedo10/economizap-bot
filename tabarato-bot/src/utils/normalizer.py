"""
Text normalization utilities for product comparison.
Normalizes product names to enable similarity matching.
"""

import re
import unicodedata
from typing import List, Set
from fuzzywuzzy import fuzz

from src.utils.logger import get_logger

logger = get_logger(__name__)


class ProductNormalizer:
    """
    Normalizes product names for comparison.
    """
    
    # Common words to remove (stop words in Portuguese)
    STOP_WORDS: Set[str] = {
        'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'do', 'da', 'dos', 'das',
        'em', 'no', 'na', 'nos', 'nas', 'para', 'com', 'por', 'e',
        'novo', 'nova', 'original', 'oficial', 'nacional', 'importado',
        'preto', 'branco', 'azul', 'vermelho', 'verde', 'amarelo',
        'gratis', 'frete', 'entrega', 'rapida', 'envio'
    }
    
    # Common brand abbreviations
    BRAND_NORMALIZATIONS = {
        'hp': 'hewlett packard',
        'dell': 'dell',
        'asus': 'asus',
        'acer': 'acer',
        'lenovo': 'lenovo',
        'samsung': 'samsung',
        'lg': 'lg',
        'apple': 'apple',
        'iphone': 'iphone',
        'xiaomi': 'xiaomi',
        'motorola': 'motorola',
        'moto': 'motorola',
    }
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize text for comparison.
        
        Args:
            text: Text to normalize
            
        Returns:
            str: Normalized text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        normalized = text.lower()
        
        # Remove accents
        normalized = ProductNormalizer._remove_accents(normalized)
        
        # Remove special characters (keep letters, numbers, spaces)
        normalized = re.sub(r'[^a-z0-9\s]', ' ', normalized)
        
        # Remove extra whitespace
        normalized = ' '.join(normalized.split())
        
        return normalized
    
    @staticmethod
    def _remove_accents(text: str) -> str:
        """
        Remove accents from text.
        
        Args:
            text: Text with accents
            
        Returns:
            str: Text without accents
        """
        # Normalize to NFD (decomposed form)
        nfd = unicodedata.normalize('NFD', text)
        
        # Filter out combining characters (accents)
        without_accents = ''.join(
            char for char in nfd
            if unicodedata.category(char) != 'Mn'
        )
        
        return without_accents
    
    @staticmethod
    def extract_keywords(text: str, min_length: int = 2) -> List[str]:
        """
        Extract important keywords from text.
        
        Args:
            text: Text to extract keywords from
            min_length: Minimum keyword length
            
        Returns:
            List[str]: List of keywords
        """
        # Normalize text
        normalized = ProductNormalizer.normalize_text(text)
        
        # Split into words
        words = normalized.split()
        
        # Filter out stop words and short words
        keywords = [
            word for word in words
            if len(word) >= min_length and word not in ProductNormalizer.STOP_WORDS
        ]
        
        return keywords
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts.
        
        Uses fuzzy string matching to calculate similarity percentage.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            float: Similarity percentage (0-100)
        """
        # Normalize both texts
        norm1 = ProductNormalizer.normalize_text(text1)
        norm2 = ProductNormalizer.normalize_text(text2)
        
        # Calculate token sort ratio (best for product names)
        # This handles word order differences
        similarity = fuzz.token_sort_ratio(norm1, norm2)
        
        return float(similarity)
    
    @staticmethod
    def are_similar(
        text1: str,
        text2: str,
        threshold: float = 70.0
    ) -> bool:
        """
        Check if two texts are similar.
        
        Args:
            text1: First text
            text2: Second text
            threshold: Similarity threshold (0-100)
            
        Returns:
            bool: True if similarity >= threshold
        """
        similarity = ProductNormalizer.calculate_similarity(text1, text2)
        return similarity >= threshold
    
    @staticmethod
    def extract_specs(text: str) -> dict:
        """
        Extract common specifications from product name.
        
        Args:
            text: Product name
            
        Returns:
            dict: Extracted specifications
        """
        specs = {}
        normalized = ProductNormalizer.normalize_text(text)
        
        # Extract RAM (e.g., "8gb", "16gb")
        ram_match = re.search(r'(\d+)\s*gb(?:\s+ram)?', normalized)
        if ram_match:
            specs['ram'] = f"{ram_match.group(1)}gb"
        
        # Extract storage (e.g., "256gb ssd", "1tb")
        storage_match = re.search(r'(\d+)\s*(gb|tb)(?:\s+ssd|\s+hdd)?', normalized)
        if storage_match:
            specs['storage'] = f"{storage_match.group(1)}{storage_match.group(2)}"
        
        # Extract processor (e.g., "i5", "i7", "ryzen 5")
        processor_match = re.search(r'(i[3579]|ryzen\s*[3579]|core\s*[3579])', normalized)
        if processor_match:
            specs['processor'] = processor_match.group(1).replace(' ', '')
        
        # Extract screen size (e.g., "15.6", "13.3")
        screen_match = re.search(r'(\d+\.?\d*)\s*(?:polegadas|pol|")', normalized)
        if screen_match:
            specs['screen'] = f"{screen_match.group(1)}in"
        
        return specs
    
    @staticmethod
    def normalize_brand(text: str) -> str:
        """
        Normalize brand names.
        
        Args:
            text: Text containing brand name
            
        Returns:
            str: Normalized brand
        """
        normalized = ProductNormalizer.normalize_text(text)
        
        for abbrev, full_name in ProductNormalizer.BRAND_NORMALIZATIONS.items():
            if abbrev in normalized.split():
                return full_name
        
        return normalized


def group_similar_products(products: List, threshold: float = 70.0) -> List[List]:
    """
    Group similar products together.
    
    Args:
        products: List of Product objects
        threshold: Similarity threshold (0-100)
        
    Returns:
        List[List]: List of product groups
    """
    if not products:
        return []
    
    groups = []
    used_indices = set()
    
    for i, product1 in enumerate(products):
        if i in used_indices:
            continue
        
        # Start a new group
        group = [product1]
        used_indices.add(i)
        
        # Find similar products
        for j, product2 in enumerate(products):
            if j <= i or j in used_indices:
                continue
            
            # Check similarity
            if ProductNormalizer.are_similar(
                product1.name,
                product2.name,
                threshold
            ):
                group.append(product2)
                used_indices.add(j)
        
        groups.append(group)
    
    logger.info(f"Grouped {len(products)} products into {len(groups)} groups")
    
    return groups
