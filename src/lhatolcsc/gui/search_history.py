"""
Search History Manager - Manages persistent search history for components.
"""

import json
from typing import List
from pathlib import Path


class SearchHistoryManager:
    """Manages search history with persistence."""
    
    def __init__(self, config_dir: str = None, max_history: int = 100):
        """
        Initialize search history manager.
        
        Args:
            config_dir: Directory to store history file (default: user config dir)
            max_history: Maximum number of history items to keep
        """
        self.max_history = max_history
        
        # Determine config directory
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            # Use user's config directory
            self.config_dir = Path.home() / ".lhatolcsc"
        
        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)
        
        # History file path
        self.history_file = self.config_dir / "search_history.json"
        
        # Load existing history
        self.history: List[str] = self._load_history()
    
    def _load_history(self) -> List[str]:
        """Load search history from file."""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Ensure it's a list and contains only strings
                    if isinstance(data, list):
                        return [str(item) for item in data if item and str(item).strip()]
            return []
        except (json.JSONDecodeError, IOError, OSError) as e:
            print(f"Warning: Could not load search history: {e}")
            return []
    
    def _save_history(self) -> None:
        """Save search history to file."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except (IOError, OSError) as e:
            print(f"Warning: Could not save search history: {e}")
    
    def add_search(self, search_term: str) -> None:
        """
        Add a search term to history.
        
        Args:
            search_term: The search term to add
        """
        # Clean and validate search term
        search_term = search_term.strip()
        if not search_term or len(search_term) < 2:
            return
        
        # Remove if already exists (to move to top)
        if search_term in self.history:
            self.history.remove(search_term)
        
        # Add to beginning of list
        self.history.insert(0, search_term)
        
        # Trim to max history size
        if len(self.history) > self.max_history:
            self.history = self.history[:self.max_history]
        
        # Save to file
        self._save_history()
    
    def get_history(self) -> List[str]:
        """Get search history list (most recent first)."""
        return self.history.copy()
    
    def clear_history(self) -> None:
        """Clear all search history."""
        self.history.clear()
        self._save_history()
    
    def remove_search(self, search_term: str) -> None:
        """
        Remove a specific search term from history.
        
        Args:
            search_term: The search term to remove
        """
        if search_term in self.history:
            self.history.remove(search_term)
            self._save_history()
    
    def get_filtered_history(self, prefix: str) -> List[str]:
        """
        Get history items that start with the given prefix.
        
        Args:
            prefix: Prefix to filter by
            
        Returns:
            List of matching history items
        """
        if not prefix:
            return self.get_history()
        
        prefix_lower = prefix.lower()
        return [item for item in self.history if item.lower().startswith(prefix_lower)]


# Global instance for the application
search_history_manager = SearchHistoryManager()
