#!/usr/bin/env python3
"""Test fixed column widths and horizontal scrolling."""

import sys
import tkinter as tk

sys.path.insert(0, 'src')

from lhatolcsc.gui.stock_browser import StockBrowserWindow
from lhatolcsc.api.client import LCSCClient
from lhatolcsc.core.config import Config


def main():
    """Test column stretching behavior."""
    try:
        # Create main window
        root = tk.Tk()
        root.title("Column Width Test")
        root.geometry("400x300+100+100")
        
        # Create stock browser
        config = Config()
        api_client = LCSCClient(
            base_url="http://localhost:5000",
            api_key="test",
            api_secret="test"
        )
        
        stock_browser = StockBrowserWindow(root, api_client, config)
        
        # Start in a narrow window to force horizontal scrolling
        stock_browser.window.geometry("600x700+100+100")
        
        print("=== COLUMN WIDTH BEHAVIOR TEST ===")
        print("Stock Browser opened in narrow window to test column behavior.")
        print("")
        print("Test Instructions:")
        print("1. Click 'List All Stock' to load data")
        print("2. Verify horizontal scrollbar appears")
        print("3. Resize window to be very narrow")
        print("4. Check that columns maintain fixed widths")
        print("5. Try fullscreen (F11) and back - columns should stay fixed")
        print("")
        print("Expected behavior:")
        print("- Columns should NOT compress to fit window")
        print("- Horizontal scrollbar should always be available")
        print("- Column widths should remain constant regardless of window size")
        print("- After fullscreen toggle, columns keep fixed widths")
        print("=================================")
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()