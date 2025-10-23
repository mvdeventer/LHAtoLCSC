"""Simple test to verify GUI appears"""
import tkinter as tk
from tkinter import messagebox

def main():
    try:
        root = tk.Tk()
        root.title("LHAtoLCSC Test")
        root.geometry("400x200")
        
        label = tk.Label(root, text="If you see this, the GUI is working!", font=("Arial", 14))
        label.pack(pady=50)
        
        button = tk.Button(root, text="Click Me", command=lambda: messagebox.showinfo("Test", "Button works!"))
        button.pack()
        
        root.mainloop()
        print("GUI closed normally")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
