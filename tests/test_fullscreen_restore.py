#!/usr/bin/env python3
"""Test fullscreen geometry restoration."""

import sys
import tkinter as tk

sys.path.insert(0, 'src')

from lhatolcsc.gui.stock_browser import StockBrowserWindow
from lhatolcsc.api.client import LCSCClient
from lhatolcsc.core.config import Config


def main():
    """Test fullscreen geometry restoration."""
    try:
        # Create main window
        root = tk.Tk()
        root.title("Fullscreen Test")
        root.geometry("300x200+100+100")
        
        # Create stock browser
        config = Config()
        api_client = LCSCClient(
            base_url="http://localhost:5000",
            api_key="test",
            api_secret="test"
        )
        
        stock_browser = StockBrowserWindow(root, api_client, config)
        
        # Position for testing - simulate dragging to left side
        stock_browser.window.geometry("960x1040+0+0")  # Left half of 1920x1080 screen
        
        print("=== FULLSCREEN GEOMETRY TEST ===")
        print("Stock Browser positioned as if dragged to left side of screen.")
        print("")
        print("Test Instructions:")
        print("1. Note the current window position and size")
        print("2. Press F11 to enter fullscreen mode")
        print("3. Press F11 again to exit fullscreen mode")
        print("4. Verify window returns to EXACT same position and size")
        print("")
        print("Expected behavior:")
        print("- Window should return to left-side split screen position")
        print("- Size should be exactly the same as before fullscreen")
        print("- No compression or distortion should occur")
        print("- Position should be preserved (left edge of screen)")
        print("==============================")
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()