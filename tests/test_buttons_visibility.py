#!/usr/bin/env python3
"""Focused test for window control buttons visibility."""

import sys
import tkinter as tk

sys.path.insert(0, 'src')

from lhatolcsc.gui.stock_browser import StockBrowserWindow
from lhatolcsc.api.client import LCSCClient
from lhatolcsc.core.config import Config


def main():
    """Test window controls with minimal setup."""
    try:
        # Create minimal config
        config = Config()
        
        # Create mock API client
        api_client = LCSCClient(
            base_url="http://localhost:5000",
            api_key="test",
            api_secret="test"
        )
        
        # Create main window
        root = tk.Tk()
        root.withdraw()
        
        # Create stock browser
        browser = StockBrowserWindow(root, api_client, config)
        
        # Add debugging
        print("=== WINDOW CONTROLS TEST ===")
        print("✅ Standard Windows title bar controls now enabled!")
        print("Look in the TOP-RIGHT corner of the window title bar for:")
        print("  🗕 Minimize button")
        print("  🗖 Maximize/Restore button") 
        print("  ❌ Close button")
        print("")
        print("Additional features:")
        print("  F11 = Toggle fullscreen mode")
        print("  Standard Windows shortcuts work (Alt+F4, etc.)")
        print("===============================")
        
        # Start the event loop
        root.mainloop()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()