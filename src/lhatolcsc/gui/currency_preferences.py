"""
Currency Preferences Manager - Manages persistent currency selection.
"""

import json
from pathlib import Path
from typing import Optional


class CurrencyPreferencesManager:
    """Manages currency preference with persistence."""

    def __init__(self, config_dir: Optional[str] = None, default_currency: str = "USD"):
        """
        Initialize currency preferences manager.

        Args:
            config_dir: Directory to store preferences file (default: user config dir)
            default_currency: Default currency if none saved
        """
        self.default_currency = default_currency

        # Determine config directory
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            # Use user's config directory
            self.config_dir = Path.home() / ".lhatolcsc"

        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)

        # Preferences file path
        self.preferences_file = self.config_dir / "currency_preferences.json"

        # Load existing preferences
        self.preferences = self._load_preferences()

    def _load_preferences(self) -> dict:
        """Load currency preferences from file."""
        try:
            if self.preferences_file.exists():
                with open(self.preferences_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Ensure it's a dict and has expected structure
                    if isinstance(data, dict):
                        return data
            return {}
        except (json.JSONDecodeError, IOError, OSError) as e:
            print(f"Error loading currency preferences: {e}")
            return {}

    def _save_preferences(self) -> bool:
        """Save currency preferences to file."""
        try:
            with open(self.preferences_file, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, indent=2, ensure_ascii=False)
            return True
        except (IOError, OSError) as e:
            print(f"Error saving currency preferences: {e}")
            return False

    def get_currency(self) -> str:
        """
        Get the saved currency preference.

        Returns:
            str: Currency code (e.g., 'USD', 'EUR')
        """
        return self.preferences.get('currency', self.default_currency)

    def set_currency(self, currency_code: str) -> bool:
        """
        Save currency preference.

        Args:
            currency_code: Currency code to save (e.g., 'USD', 'EUR')

        Returns:
            bool: True if saved successfully, False otherwise
        """
        if not currency_code or not isinstance(currency_code, str):
            return False

        # Normalize currency code (uppercase)
        currency_code = currency_code.upper().strip()

        # Update preferences
        self.preferences['currency'] = currency_code

        # Save to file
        return self._save_preferences()

    def reset_currency(self) -> bool:
        """
        Reset currency to default.

        Returns:
            bool: True if reset successfully, False otherwise
        """
        return self.set_currency(self.default_currency)

    def get_preferences_file_path(self) -> str:
        """
        Get the path to the preferences file.

        Returns:
            str: Full path to preferences file
        """
        return str(self.preferences_file)


# Create a default instance for easy access
currency_preferences = CurrencyPreferencesManager()
