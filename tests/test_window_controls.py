#!/usr/bin/env python3
"""Test script for window controls functionality."""

import sys
import tkinter as tk

sys.path.insert(0, 'src')

from lhatolcsc.gui.stock_browser import StockBrowserWindow
from lhatolcsc.api.client import LCSCClient
from lhatolcsc.core.config import Config


def main():
    """Test the stock browser window controls."""
    try:
        # Create a minimal config
        config = Config()
        
        # Create a mock API client
        api_client = LCSCClient(
            base_url="http://localhost:5000",
            api_key="test",
            api_secret="test"
        )
        
        # Create the main window
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        # Create the stock browser window
        StockBrowserWindow(root, api_client, config)
        
        print("Stock Browser Window opened successfully!")
        print("Test the following features:")
        print("1. Click the 'Minimize' button or press Ctrl+M")
        print("2. Click the 'Fullscreen' button or press F11/Alt+Return")
        print("3. Close the window to exit")
        
        # Start the GUI event loop
        root.mainloop()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()