#!/usr/bin/env python3
"""Test to verify Windows title bar controls are visible."""

import sys
import tkinter as tk

sys.path.insert(0, 'src')

from lhatolcsc.gui.stock_browser import StockBrowserWindow
from lhatolcsc.api.client import LCSCClient
from lhatolcsc.core.config import Config


def test_simple_window():
    """Test a simple toplevel window to compare."""
    simple = tk.Toplevel()
    simple.title("Simple Test Window - Should have Min/Max/Close")
    simple.geometry("400x300")
    simple.resizable(True, True)
    
    tk.Label(simple, text="This is a simple window.\nCheck title bar for Min/Max/Close buttons", 
             justify=tk.CENTER, pady=50).pack()
    
    return simple


def main():
    """Test window controls."""
    try:
        root = tk.Tk()
        root.title("Root Window")
        root.geometry("300x200")
        
        # Create simple test window first
        simple_window = test_simple_window()
        
        # Create minimal config
        config = Config()
        
        # Create mock API client
        api_client = LCSCClient(
            base_url="http://localhost:5000",
            api_key="test",
            api_secret="test"
        )
        
        # Create stock browser
        StockBrowserWindow(root, api_client, config)
        
        print("=== TITLE BAR CONTROLS TEST ===")
        print("Two windows should now be open:")
        print("1. 'Simple Test Window' - Should have Min/Max/Close buttons")
        print("2. 'Stock Browser' - Should also have Min/Max/Close buttons")
        print("")
        print("If the Stock Browser is missing buttons but Simple Window has them,")
        print("then we know the issue is in the Stock Browser configuration.")
        print("===============================")
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()