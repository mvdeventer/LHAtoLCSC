"""
Professional Theme Manager for Stock Application.

Provides a modern, corporate color scheme suitable for inventory management.
"""

import tkinter as tk
from tkinter import ttk


class CorporateTheme:
    """Professional corporate theme with modern colors."""
    
    # Primary color palette - Professional Blue & Gray
    PRIMARY_DARK = "#1e3a5f"      # Deep Navy Blue (headers, sidebars)
    PRIMARY = "#2c5f8d"           # Corporate Blue (primary actions)
    PRIMARY_LIGHT = "#4a7ba7"     # Light Blue (hover states)
    
    # Accent colors
    ACCENT = "#ff6b35"            # Warm Orange (important actions)
    ACCENT_LIGHT = "#ff8856"      # Light Orange (hover)
    SUCCESS = "#27ae60"           # Green (success states)
    WARNING = "#f39c12"           # Amber (warnings)
    ERROR = "#e74c3c"             # Red (errors)
    INFO = "#3498db"              # Sky Blue (info)
    
    # Neutral colors
    BACKGROUND = "#f5f7fa"        # Light Gray (main background)
    SURFACE = "#ffffff"           # White (cards, panels)
    SURFACE_DARK = "#ecf0f1"      # Light Gray (alternate rows)
    BORDER = "#d5dbdb"            # Gray (borders)
    BORDER_DARK = "#95a5a6"       # Dark Gray (focused borders)
    
    # Text colors
    TEXT_PRIMARY = "#2c3e50"      # Dark Gray (main text)
    TEXT_SECONDARY = "#7f8c8d"    # Medium Gray (secondary text)
    TEXT_LIGHT = "#ffffff"        # White (text on dark backgrounds)
    TEXT_DISABLED = "#bdc3c7"     # Light Gray (disabled text)
    
    # Data grid colors
    GRID_HEADER = "#34495e"       # Dark Slate (table headers)
    GRID_ROW_EVEN = "#ffffff"     # White (even rows)
    GRID_ROW_ODD = "#f8f9fa"      # Very Light Gray (odd rows)
    GRID_SELECTED = "#3498db"     # Blue (selected row)
    GRID_HOVER = "#e8f4f8"        # Light Blue (hover row)
    
    # Status bar colors
    STATUS_BG = "#34495e"         # Dark Slate
    STATUS_FG = "#ecf0f1"         # Light Gray
    
    # Button colors
    BUTTON_PRIMARY = "#2c5f8d"    # Corporate Blue
    BUTTON_PRIMARY_HOVER = "#4a7ba7"
    BUTTON_SECONDARY = "#95a5a6"  # Gray
    BUTTON_SECONDARY_HOVER = "#7f8c8d"
    BUTTON_SUCCESS = "#27ae60"    # Green
    BUTTON_DANGER = "#e74c3c"     # Red
    
    # Font settings
    FONT_FAMILY = "Segoe UI"      # Modern sans-serif (Windows)
    FONT_SIZE_NORMAL = 9
    FONT_SIZE_LARGE = 11
    FONT_SIZE_HEADER = 14
    FONT_SIZE_TITLE = 16
    
    @classmethod
    def apply_to_root(cls, root: tk.Tk):
        """Apply corporate theme to root window and all widgets."""
        # Configure root window
        root.configure(bg=cls.BACKGROUND)
        
        # Create custom ttk style
        style = ttk.Style(root)
        style.theme_use('clam')  # Use 'clam' as base for better customization
        
        # Configure TFrame
        style.configure(
            "TFrame",
            background=cls.BACKGROUND
        )
        
        # Configure TLabel
        style.configure(
            "TLabel",
            background=cls.BACKGROUND,
            foreground=cls.TEXT_PRIMARY,
            font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL)
        )
        
        # Header label style
        style.configure(
            "Header.TLabel",
            background=cls.BACKGROUND,
            foreground=cls.PRIMARY_DARK,
            font=(cls.FONT_FAMILY, cls.FONT_SIZE_HEADER, "bold")
        )
        
        # Title label style
        style.configure(
            "Title.TLabel",
            background=cls.BACKGROUND,
            foreground=cls.PRIMARY_DARK,
            font=(cls.FONT_FAMILY, cls.FONT_SIZE_TITLE, "bold")
        )
        
        # Secondary label style
        style.configure(
            "Secondary.TLabel",
            background=cls.BACKGROUND,
            foreground=cls.TEXT_SECONDARY,
            font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL)
        )
        
        # Configure TButton
        style.configure(
            "TButton",
            background=cls.BUTTON_PRIMARY,
            foreground=cls.TEXT_LIGHT,
            bordercolor=cls.BUTTON_PRIMARY,
            lightcolor=cls.BUTTON_PRIMARY,
            darkcolor=cls.BUTTON_PRIMARY,
            font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL, "bold"),
            padding=(10, 5),
            relief=tk.FLAT
        )
        
        style.map(
            "TButton",
            background=[
                ("active", cls.BUTTON_PRIMARY_HOVER),
                ("pressed", cls.PRIMARY_DARK),
                ("disabled", cls.TEXT_DISABLED)
            ],
            foreground=[
                ("disabled", cls.TEXT_SECONDARY)
            ]
        )
        
        # Accent button style
        style.configure(
            "Accent.TButton",
            background=cls.ACCENT,
            foreground=cls.TEXT_LIGHT,
            font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL, "bold"),
            padding=(12, 6)
        )
        
        style.map(
            "Accent.TButton",
            background=[
                ("active", cls.ACCENT_LIGHT),
                ("pressed", cls.ACCENT)
            ]
        )
        
        # Success button style
        style.configure(
            "Success.TButton",
            background=cls.SUCCESS,
            foreground=cls.TEXT_LIGHT
        )
        
        # Danger button style
        style.configure(
            "Danger.TButton",
            background=cls.ERROR,
            foreground=cls.TEXT_LIGHT
        )
        
        # Configure TEntry
        style.configure(
            "TEntry",
            fieldbackground=cls.SURFACE,
            foreground=cls.TEXT_PRIMARY,
            bordercolor=cls.BORDER,
            lightcolor=cls.BORDER,
            darkcolor=cls.BORDER,
            font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL),
            padding=5
        )
        
        style.map(
            "TEntry",
            fieldbackground=[("focus", cls.SURFACE)],
            bordercolor=[("focus", cls.PRIMARY)],
            lightcolor=[("focus", cls.PRIMARY)],
            darkcolor=[("focus", cls.PRIMARY)]
        )
        
        # Configure TCombobox
        style.configure(
            "TCombobox",
            fieldbackground=cls.SURFACE,
            background=cls.SURFACE,
            foreground=cls.TEXT_PRIMARY,
            bordercolor=cls.BORDER,
            arrowcolor=cls.PRIMARY,
            font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL),
            padding=5
        )
        
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", cls.SURFACE)],
            background=[("readonly", cls.SURFACE)],
            bordercolor=[("focus", cls.PRIMARY)]
        )
        
        # Configure Treeview (data grids)
        style.configure(
            "Treeview",
            background=cls.SURFACE,
            foreground=cls.TEXT_PRIMARY,
            fieldbackground=cls.SURFACE,
            bordercolor=cls.BORDER,
            font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL),
            rowheight=25
        )
        
        style.configure(
            "Treeview.Heading",
            background=cls.GRID_HEADER,
            foreground=cls.TEXT_LIGHT,
            bordercolor=cls.GRID_HEADER,
            font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL, "bold"),
            padding=8
        )
        
        style.map(
            "Treeview.Heading",
            background=[("active", cls.PRIMARY_DARK)],
            relief=[("active", tk.FLAT)]
        )
        
        style.map(
            "Treeview",
            background=[
                ("selected", cls.GRID_SELECTED),
                ("!selected", cls.SURFACE)
            ],
            foreground=[
                ("selected", cls.TEXT_LIGHT),
                ("!selected", cls.TEXT_PRIMARY)
            ]
        )
        
        # Configure TLabelframe
        style.configure(
            "TLabelframe",
            background=cls.BACKGROUND,
            foreground=cls.PRIMARY_DARK,
            bordercolor=cls.BORDER,
            font=(cls.FONT_FAMILY, cls.FONT_SIZE_LARGE, "bold"),
            relief=tk.FLAT
        )
        
        style.configure(
            "TLabelframe.Label",
            background=cls.BACKGROUND,
            foreground=cls.PRIMARY_DARK,
            font=(cls.FONT_FAMILY, cls.FONT_SIZE_LARGE, "bold")
        )
        
        # Configure TNotebook (tabs)
        style.configure(
            "TNotebook",
            background=cls.BACKGROUND,
            bordercolor=cls.BORDER,
            tabmargins=[2, 5, 2, 0]
        )
        
        style.configure(
            "TNotebook.Tab",
            background=cls.SURFACE_DARK,
            foreground=cls.TEXT_PRIMARY,
            bordercolor=cls.BORDER,
            font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL),
            padding=[20, 8]
        )
        
        style.map(
            "TNotebook.Tab",
            background=[
                ("selected", cls.SURFACE),
                ("active", cls.PRIMARY_LIGHT)
            ],
            foreground=[
                ("selected", cls.PRIMARY_DARK),
                ("active", cls.TEXT_LIGHT)
            ]
        )
        
        # Configure TProgressbar
        style.configure(
            "TProgressbar",
            background=cls.PRIMARY,
            troughcolor=cls.SURFACE_DARK,
            bordercolor=cls.BORDER,
            lightcolor=cls.PRIMARY,
            darkcolor=cls.PRIMARY
        )
        
        # Configure TScrollbar
        style.configure(
            "TScrollbar",
            background=cls.SURFACE_DARK,
            troughcolor=cls.BACKGROUND,
            bordercolor=cls.BORDER,
            arrowcolor=cls.TEXT_SECONDARY
        )
        
        style.map(
            "TScrollbar",
            background=[("active", cls.BORDER_DARK)]
        )
        
        return style
    
    @classmethod
    def apply_to_toplevel(cls, window: tk.Toplevel):
        """Apply theme to a Toplevel window."""
        window.configure(bg=cls.BACKGROUND)
    
    @classmethod
    def create_status_bar(cls, parent, textvariable) -> tk.Label:
        """Create a themed status bar."""
        return tk.Label(
            parent,
            textvariable=textvariable,
            bg=cls.STATUS_BG,
            fg=cls.STATUS_FG,
            font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL),
            relief=tk.FLAT,
            anchor=tk.W,
            padx=10,
            pady=5
        )
    
    @classmethod
    def create_header_frame(cls, parent) -> tk.Frame:
        """Create a themed header frame."""
        return tk.Frame(
            parent,
            bg=cls.PRIMARY_DARK,
            height=60
        )
