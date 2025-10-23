#!/usr/bin/env python3
"""Test horizontal scrolling and split screen behavior."""

import sys
import tkinter as tk

sys.path.insert(0, 'src')

from lhatolcsc.gui.stock_browser import StockBrowserWindow
from lhatolcsc.api.client import LCSCClient
from lhatolcsc.core.config import Config


def main():
    """Test horizontal scrolling functionality."""
    try:
        # Create main window
        root = tk.Tk()
        root.title("Main Window")
        root.geometry("400x600+50+50")
        
        # Add test content
        tk.Label(root, text="Main Window\nfor split screen test", 
                justify=tk.CENTER, pady=100).pack()
        
        # Create stock browser positioned for testing
        config = Config()
        api_client = LCSCClient(
            base_url="http://localhost:5000",
            api_key="test",
            api_secret="test"
        )
        
        stock_browser = StockBrowserWindow(root, api_client, config)
        
        # Position browser to test split screen - smaller window
        stock_browser.window.geometry("800x600+500+50")
        
        print("=== HORIZONTAL SCROLLING TEST ===")
        print("Stock Browser should now be open in a smaller window.")
        print("")
        print("Test Instructions:")
        print("1. Click 'List All Stock' to load products")
        print("2. Try to drag the window to half-screen (Win+Left)")
        print("3. Check that horizontal scrollbar appears")
        print("4. Test horizontal scrolling with mouse wheel or drag")
        print("5. Verify all columns are accessible")
        print("")
        print("Expected behavior:")
        print("- Window should resize properly to half-screen")
        print("- Horizontal scrollbar should be functional")
        print("- All price columns should be accessible via scrolling")
        print("================================")
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()