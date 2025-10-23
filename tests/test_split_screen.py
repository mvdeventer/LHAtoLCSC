#!/usr/bin/env python3
"""Test split screen functionality and scrollbar behavior."""

import sys
import tkinter as tk

sys.path.insert(0, 'src')

from lhatolcsc.gui.stock_browser import StockBrowserWindow
from lhatolcsc.api.client import LCSCClient
from lhatolcsc.core.config import Config


def main():
    """Test split screen behavior."""
    try:
        # Create main window positioned on left
        root = tk.Tk()
        root.title("Main Window (Left Side)")
        root.geometry("500x600+100+100")
        
        # Add some scrollable content to main window
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        main_scroll = tk.Scrollbar(main_frame)
        main_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        main_listbox = tk.Listbox(main_frame, yscrollcommand=main_scroll.set)
        for i in range(100):
            main_listbox.insert(tk.END, f"Main window item {i+1}")
        main_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        main_scroll.config(command=main_listbox.yview)
        
        # Create a test window on the right
        test_window = tk.Toplevel(root)
        test_window.title("Test Window (Right Side)")
        test_window.geometry("500x600+650+100")
        
        # Add scrollable content to test window
        test_frame = tk.Frame(test_window)
        test_frame.pack(fill=tk.BOTH, expand=True)
        
        test_scroll = tk.Scrollbar(test_frame)
        test_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        test_listbox = tk.Listbox(test_frame, yscrollcommand=test_scroll.set)
        for i in range(100):
            test_listbox.insert(tk.END, f"Right window item {i+1}")
        test_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        test_scroll.config(command=test_listbox.yview)
        
        # Create stock browser
        config = Config()
        api_client = LCSCClient(
            base_url="http://localhost:5000",
            api_key="test",
            api_secret="test"
        )
        
        stock_browser = StockBrowserWindow(root, api_client, config)
        # Position stock browser on the left
        stock_browser.window.geometry("800x700+50+50")
        
        print("=== SPLIT SCREEN TEST ===")
        print("Three windows should be open:")
        print("1. Main Window (Left) - with scrollable list")
        print("2. Test Window (Right) - with scrollable list") 
        print("3. Stock Browser - should work in split screen")
        print("")
        print("Test Instructions:")
        print("1. Drag Stock Browser to left side of screen")
        print("2. Position Test Window on right side")
        print("3. Click in Test Window to focus it")
        print("4. Try scrolling in Stock Browser - should still work!")
        print("========================")
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()