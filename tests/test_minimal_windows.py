#!/usr/bin/env python3
"""Minimal window test to diagnose title bar button issues."""

import tkinter as tk


def main():
    """Create minimal windows to test title bar controls."""
    root = tk.Tk()
    root.title("Root Window")
    root.geometry("300x200")
    
    # Test 1: Basic Toplevel
    window1 = tk.Toplevel(root)
    window1.title("Test 1: Basic Toplevel - Check for Min/Max/Close")
    window1.geometry("400x300")
    window1.resizable(True, True)
    
    label1 = tk.Label(window1, text="Basic Toplevel Window\nShould have Min/Max/Close buttons", 
                     justify=tk.CENTER, pady=50)
    label1.pack()
    
    # Test 2: Toplevel with modal grab
    window2 = tk.Toplevel(root)
    window2.title("Test 2: Modal Grab - Check for Min/Max/Close")
    window2.geometry("400x300+50+50")
    window2.resizable(True, True)
    window2.grab_set()
    
    label2 = tk.Label(window2, text="Modal Grab Window\nShould still have Min/Max/Close buttons", 
                     justify=tk.CENTER, pady=50)
    label2.pack()
    
    # Test 3: Toplevel with transient
    window3 = tk.Toplevel(root)
    window3.title("Test 3: Transient - Check for Min/Max/Close")
    window3.geometry("400x300+100+100")
    window3.resizable(True, True)
    window3.transient(root)
    
    label3 = tk.Label(window3, text="Transient Window\nMight be missing Min/Max buttons", 
                     justify=tk.CENTER, pady=50)
    label3.pack()
    
    print("=== WINDOW TITLE BAR TEST ===")
    print("Three test windows should be open:")
    print("1. Basic Toplevel - Should have all buttons")
    print("2. Modal Grab - Should have all buttons")  
    print("3. Transient - Might be missing Min/Max buttons")
    print("")
    print("This will help identify which setting removes the title bar buttons.")
    print("============================")
    
    root.mainloop()


if __name__ == "__main__":
    main()