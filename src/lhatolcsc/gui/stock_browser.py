"""
Stock Browser Window - Debug tool for viewing mock server inventory.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Optional
from io import BytesIO
import requests
from PIL import Image, ImageTk, ImageDraw
import threading
import webbrowser

from lhatolcsc.api.client import LCSCClient
from lhatolcsc.core.config import Config
from lhatolcsc.gui.theme import CorporateTheme
from lhatolcsc.gui.currency_converter import currency_converter
from lhatolcsc.gui.currency_preferences import currency_preferences
from lhatolcsc.gui.search_history import SearchHistoryManager

logger = logging.getLogger(__name__)


class StockBrowserWindow:
    """Window for browsing stock from LCSC API (debug feature)."""
    
    def __init__(self, parent: tk.Tk, api_client: LCSCClient, config: Config):
        """
        Initialize stock browser window.
        
        Args:
            parent: Parent window
            api_client: LCSC API client
            config: Application configuration
        """
        self.parent = parent
        self.api_client = api_client
        self.config = config
        self.products = []
        self.current_page = 1
        self.total_pages = 1
        self.page_size = 10  # Changed to 10 for faster loading
        
        # Image cache to keep references to PhotoImage objects
        self.image_cache = {}
        self.load_images = False  # Disabled by default for speed
        
        # Sorting state
        self.sort_column = None
        self.sort_reverse = False
        
        # Currency conversion state
        saved_currency = currency_preferences.get_currency()
        self.current_currency = tk.StringVar(value=saved_currency)
        self.currency_symbols = currency_converter.get_supported_currencies()
        
        # Search history manager
        self.search_history_manager = SearchHistoryManager()
        
        # Window state tracking
        self.is_fullscreen = False
        self.is_minimized = False
        self.normal_geometry = "1200x700"  # Default size for restoration
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title(f"Stock Browser (Debug) - {config.app_name} v{config.version}")
        self.window.geometry("1200x700")  # More reasonable default size for split screen
        self.window.minsize(800, 500)  # Allow smaller sizes for split screen
        
        # Ensure window has ALL standard title bar controls
        self.window.resizable(True, True)  # Enable resize handles
        self.window.attributes('-topmost', False)  # Don't force always on top
        
        # Explicitly ensure title bar buttons are available (Windows-specific)
        try:
            # For Windows, ensure the window has proper decorations
            self.window.attributes('-toolwindow', False)  # Show in taskbar
            self.window.wm_attributes('-type', 'normal')  # Normal window type
        except tk.TclError:
            # These attributes might not be available on all platforms
            pass
        
        # IMPORTANT: Don't make it transient - this can hide title bar buttons
        # self.window.transient(parent)  # This removes Min/Max buttons!
        
        # Apply corporate theme AFTER window setup
        CorporateTheme.apply_to_toplevel(self.window)
        
        # Don't use modal grab - it interferes with split screen and scrollbars
        # self.window.grab_set()  # This prevents proper window interaction
        self.window.focus_set()  # Just focus the window initially
        
        # Bind keyboard shortcuts for fullscreen (minimize uses standard Windows shortcut)
        self.window.bind("<F11>", lambda e: self._toggle_fullscreen())
        self.window.bind("<Alt-Return>", lambda e: self._toggle_fullscreen())
        
        self._create_widgets()
        # Don't auto-load products - wait for user to search
        status_text = "Ready. Enter search term or click 'List All' to load products."
        self.status_var.set(status_text)
        
        # Initialize exchange rates in background
        self._update_exchange_rates()
        
        # Initialize currency column headers after UI is created
        self._update_price_column_headers("USD")

    def _create_sort_command(self, column):
        """Create a sort command for a column."""
        return lambda: self._sort_by_column(column)

    def _update_exchange_rates(self):
        """Update exchange rates in background."""
        def update_rates():
            currency_converter.update_exchange_rates()
            rate_info = currency_converter.get_rate_info()
            self.rate_info_var.set(rate_info)
        
        threading.Thread(target=update_rates, daemon=True).start()

    def _on_currency_change(self, event=None):
        """Handle currency selection change."""
        new_currency = self.current_currency.get()
        
        # Save currency preference for persistence
        currency_preferences.set_currency(new_currency)
        
        # Update column headers to show new currency symbol
        self._update_price_column_headers(new_currency)
        
        # Refresh the displayed prices if products are loaded
        if self.products:
            self._populate_tree()
    
    def _update_price_column_headers(self, currency_code: str):
        """Update price column headers with currency symbol."""
        symbol = currency_converter.get_currency_symbol(currency_code)
        
        # Update price column headers while preserving sort commands
        price_quantities = [1, 10, 25, 50, 100, 200, 500, 1000, 5000, 10000]
        for i, qty in enumerate(price_quantities):
            col_name = f"Price ({qty}+)"
            header_text = f"{symbol} ({qty}+)"
            # Preserve the sort command when updating header
            self.tree.heading(col_name, text=header_text, anchor="center",
                              command=self._create_sort_command(col_name))
    
    def _create_widgets(self):
        """Create window widgets."""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="📦 Mock Server Stock Browser",
            style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Info label
        info_label = ttk.Label(
            main_frame,
            text="Browse components available in the mock server. Search in code, model, name, and description."
        )
        info_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))
        
        # Search frame
        search_frame = ttk.LabelFrame(main_frame, text="Search", padding="10")
        search_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        
        # First row: Keyword input and history
        ttk.Label(search_frame, text="Keyword:").grid(row=0, column=0, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.grid(row=0, column=1, padx=5, sticky="ew")
        search_entry.bind('<Return>', lambda e: self._search())
        
        # Search history dropdown
        ttk.Label(search_frame, text="History:").grid(row=0, column=2, padx=(10, 5))
        self.history_var = tk.StringVar()
        self.history_combo = ttk.Combobox(
            search_frame,
            textvariable=self.history_var,
            width=25,
            state="readonly"
        )
        self.history_combo.grid(row=0, column=3, padx=5)
        self.history_combo.bind('<<ComboboxSelected>>', self._on_history_selected)
        
        # Update history dropdown with saved history
        self._update_history_dropdown()
        
        search_button = ttk.Button(search_frame, text="Search", command=self._search, style="Accent.TButton")
        search_button.grid(row=0, column=4, padx=5)
        
        clear_button = ttk.Button(search_frame, text="Clear", command=self._clear_search)
        clear_button.grid(row=0, column=5, padx=5)
        
        # Clear history button
        clear_history_button = ttk.Button(search_frame, text="Clear History", command=self._clear_history)
        clear_history_button.grid(row=0, column=6, padx=5)
        
        # Second row: Result count and currency
        self.result_count_var = tk.StringVar(value="No products loaded")
        result_label = ttk.Label(search_frame, textvariable=self.result_count_var)
        result_label.grid(row=1, column=0, columnspan=2, padx=5, sticky="w")
        
        # Currency selection
        ttk.Label(search_frame, text="Currency:").grid(row=1, column=2, padx=(10, 5))
        currency_combo = ttk.Combobox(
            search_frame,
            textvariable=self.current_currency,
            values=list(self.currency_symbols.keys()),
            width=8,
            state="readonly"
        )
        currency_combo.grid(row=1, column=3, padx=5, sticky="w")
        currency_combo.bind('<<ComboboxSelected>>', self._on_currency_change)
        
        # Exchange rate info
        self.rate_info_var = tk.StringVar(value="Loading rates...")
        rate_info_label = ttk.Label(search_frame, textvariable=self.rate_info_var, font=("Arial", 8))
        rate_info_label.grid(row=1, column=4, columnspan=3, padx=5, sticky="w")
        
        search_frame.columnconfigure(1, weight=1)
        
        # Treeview frame with proper grid configuration
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(0, 10))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollbars for treeview
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.grid(row=0, column=1, sticky="ns")
        
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Define columns - ALL 10 possible price breaks (no image column for speed)
        # Price column names will be updated based on selected currency
        self.base_columns = (
            "Product Code",
            "Model", 
            "Brand",
            "Category",
            "Package",
            "Description",
            "Stock"
        )
        
        self.price_columns = (
            "Price (1+)",
            "Price (10+)",
            "Price (25+)", 
            "Price (50+)",
            "Price (100+)",
            "Price (200+)",
            "Price (500+)",
            "Price (1000+)",
            "Price (5000+)",
            "Price (10000+)"
        )
        
        columns = self.base_columns + self.price_columns
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="tree headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            selectmode="browse"
        )
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Configure columns with fixed widths - NO stretching for proper horizontal scrolling
        self.tree.column("#0", width=0, stretch=False)
        self.tree.column("Product Code", width=80, anchor="w", stretch=False)
        self.tree.column("Model", width=120, anchor="w", stretch=False)
        self.tree.column("Brand", width=80, anchor="w", stretch=False)
        self.tree.column("Category", width=100, anchor="w", stretch=False)
        self.tree.column("Package", width=60, anchor="center", stretch=False)
        self.tree.column("Description", width=200, anchor="w", stretch=False)
        self.tree.column("Stock", width=60, anchor="e", stretch=False)
        self.tree.column("Price (1+)", width=60, anchor="e", stretch=False)
        self.tree.column("Price (10+)", width=60, anchor="e", stretch=False)
        self.tree.column("Price (25+)", width=60, anchor="e", stretch=False)
        self.tree.column("Price (50+)", width=60, anchor="e", stretch=False)
        self.tree.column("Price (100+)", width=65, anchor="e", stretch=False)
        self.tree.column("Price (200+)", width=65, anchor="e", stretch=False)
        self.tree.column("Price (500+)", width=65, anchor="e", stretch=False)
        self.tree.column("Price (1000+)", width=70, anchor="e", stretch=False)
        self.tree.column("Price (5000+)", width=70, anchor="e", stretch=False)
        self.tree.column("Price (10000+)", width=70, anchor="e", stretch=False)
        
        # Configure headings with sorting
        for col in columns:
            if col in ["Model", "Description"]:
                self.tree.heading(col, text=col, anchor="w")
            elif col in self.price_columns:
                # Price columns will be updated by _update_price_column_headers
                self.tree.heading(col, text=col, anchor="center",
                                  command=self._create_sort_command(col))
            elif col in ["Stock"]:
                self.tree.heading(col, text=col, anchor="center",
                                  command=self._create_sort_command(col))
            else:
                self.tree.heading(col, text=col, anchor="center")
        
        # Bind double-click to show details
        self.tree.bind("<Double-1>", self._on_item_double_click)
        
        # Bind mouse wheel for horizontal scrolling (Shift+Wheel)
        self.tree.bind("<Shift-MouseWheel>", self._on_horizontal_mousewheel)
        self.tree.bind("<Control-MouseWheel>", self._on_horizontal_mousewheel)
        
        # Pagination frame
        pagination_frame = ttk.Frame(main_frame)
        pagination_frame.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        
        # Left side: Page info and navigation
        left_frame = ttk.Frame(pagination_frame)
        left_frame.pack(side=tk.LEFT)
        
        self.page_info_var = tk.StringVar(value="Page 1 of 1")
        ttk.Label(left_frame, textvariable=self.page_info_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(left_frame, text="⏮️ First", command=self._first_page).pack(side=tk.LEFT, padx=5)
        ttk.Button(left_frame, text="◀ Previous", command=self._previous_page).pack(side=tk.LEFT, padx=5)
        
        # Page number buttons (1-5 pages ahead/behind)
        self.page_buttons_frame = ttk.Frame(left_frame)
        self.page_buttons_frame.pack(side=tk.LEFT, padx=10)
        self.page_buttons = []  # Store references to page buttons
        
        ttk.Button(left_frame, text="Next ▶", command=self._next_page).pack(side=tk.LEFT, padx=5)
        ttk.Button(left_frame, text="Last ⏭️", command=self._last_page).pack(side=tk.LEFT, padx=5)
        
        # Right side: Page size controls
        right_frame = ttk.Frame(pagination_frame)
        right_frame.pack(side=tk.RIGHT)
        
        ttk.Label(right_frame, text="Page size:").pack(side=tk.LEFT, padx=(20, 5))
        page_size_combo = ttk.Combobox(
            right_frame,
            values=["10", "20", "30", "40", "50", "100"],
            width=10,
            state="readonly"
        )
        page_size_combo.set(str(self.page_size))  # Convert to string for combobox
        page_size_combo.bind('<<ComboboxSelected>>', self._change_page_size)
        page_size_combo.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = CorporateTheme.create_status_bar(main_frame, self.status_var)
        status_bar.grid(row=5, column=0, columnspan=3, sticky="ew")
        
        # Buttons frame with better spacing
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=(15, 10), 
                         sticky="ew")
        
        # Configure button frame to expand
        button_frame.columnconfigure(1, weight=1)
        
        # Action buttons
        ttk.Button(button_frame, text="📋 List All Stock", 
                  command=self._list_all_stock, 
                  style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Refresh", 
                  command=self._load_products).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="💾 Export CSV", 
                  command=self._export_csv, 
                  style="Success.TButton").pack(side=tk.LEFT, padx=5)
        
        # Info label for window controls (right side)
        info_label = ttk.Label(button_frame, 
                              text="💡 F11=Fullscreen | Standard title bar for minimize/maximize",
                              foreground="gray")
        info_label.pack(side=tk.RIGHT, padx=10)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
    
    def _on_horizontal_mousewheel(self, event):
        """Handle horizontal mouse wheel scrolling."""
        # Scroll horizontally when Shift or Ctrl is held (faster scroll)
        scroll_amount = int(-1 * (event.delta / 120)) * 3  # 3x faster scrolling
        self.tree.xview_scroll(scroll_amount, "units")
    
    def _on_item_double_click(self, event):
        """Handle double-click on tree item to show product details."""
        self._show_details(event)
    
    def _load_products(self, keyword: Optional[str] = None):
        """Load products from API."""
        # Get the current search keyword from the search box
        if keyword is None:
            keyword = self.search_var.get().strip()
        
        self.status_var.set("Loading products from mock server...")
        self.window.update()
        
        try:
            # Search products using API
            search_keyword = keyword if keyword else ""
            
            result = self.api_client.search_products(
                keyword=search_keyword,
                current_page=self.current_page,
                page_size=self.page_size
            )
            
            # result is a SearchResult dataclass with products, total, current_page, page_size
            # Store LCSCProduct objects
            self.products = result.products
            total = result.total
            self.total_pages = result.total_pages
            
            self._populate_tree()
            
            self.result_count_var.set(f"Found {total} products")
            self._update_pagination_info()
            self.status_var.set(f"Loaded {len(self.products)} products (Page {self.current_page}/{self.total_pages})")
            
            # Force UI update
            self.window.update_idletasks()
            
            logger.info(f"Loaded {len(self.products)} products from mock server")
                
        except Exception as e:
            # Show error dialog (no modal grab needed)
            messagebox.showerror("Error", f"Failed to load products:\n{str(e)}")
            self.status_var.set("Error loading products")
            logger.error(f"Failed to load products: {e}", exc_info=True)
    
    def _get_thumbnail(self, image_url: str) -> Optional[ImageTk.PhotoImage]:
        """Download and create thumbnail for component image."""
        if not image_url or image_url == "":
            return None
        
        # Check cache first
        if image_url in self.image_cache:
            return self.image_cache[image_url]
        
        try:
            # Download image with proper headers (LCSC blocks requests without headers)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': 'https://www.lcsc.com/',
                'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            }
            response = requests.get(image_url, timeout=2, headers=headers)
            response.raise_for_status()
            
            # Open and resize image
            img = Image.open(BytesIO(response.content))
            img.thumbnail((50, 50), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Cache it
            self.image_cache[image_url] = photo
            return photo
            
        except Exception as e:
            logger.debug(f"Failed to load image {image_url}: {e}")
            return None
    
    def _populate_tree(self):
        """Populate treeview with products."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add products (LCSCProduct objects)
        for product in self.products:
            product_code = product.product_code or 'N/A'
            model = product.manufacturer_part or 'N/A'
            brand = product.manufacturer or 'N/A'
            package = product.package_type or 'N/A'
            
            # Truncate description to 100 chars for display and fix encoding
            description = product.description or ''
            # Replace Unicode characters with ASCII equivalents for Windows Tkinter
            # Handle both proper Unicode and double-encoded characters
            description = (description
                .replace('Ω', 'ohm').replace('Î©', 'ohm')
                .replace('±', '+/-').replace('Â±', '+/-')
                .replace('µ', 'u').replace('Âµ', 'u')
                .replace('°', 'deg').replace('Â°', 'deg')
                .replace('≤', '<=').replace('â‰¤', '<=')
                .replace('≥', '>=').replace('â‰¥', '>=')
                .replace('Å', 'A')
                .replace('â€"', '-')
                .replace('Ã—', 'x')
            )
            # Remove any remaining non-ASCII characters
            description = description.encode('ascii', 'ignore').decode('ascii')
            if len(description) > 100:
                description = description[:97] + '...'
            
            stock = str(product.stock)
            
            # Get prices from ALL 10 price tiers with currency conversion
            price_dict = {tier.quantity: tier.unit_price for tier in product.price_tiers}
            current_currency = self.current_currency.get()
            
            # Convert prices to selected currency and format appropriately
            price_quantities = [1, 10, 25, 50, 100, 200, 500,
                                1000, 5000, 10000]
            converted_prices = []
            
            for qty in price_quantities:
                if qty in price_dict and price_dict[qty] > 0:
                    formatted_price = currency_converter.format_price(
                        price_dict[qty], current_currency
                    )
                    converted_prices.append(formatted_price)
                else:
                    converted_prices.append('')
            
            (price_1, price_10, price_25, price_50, price_100,
             price_200, price_500, price_1000, price_5000,
             price_10000) = converted_prices
            
            # Get category name (if available)
            category = product.category_name if hasattr(product, 'category_name') else ''
            
            values = (
                product_code,
                model,
                brand,
                category,
                package,
                description,
                stock,
                price_1,
                price_10,
                price_25,
                price_50,
                price_100,
                price_200,
                price_500,
                price_1000,
                price_5000,
                price_10000
            )
            
            # Insert item (no images for speed)
            self.tree.insert("", tk.END, values=values, tags=(product_code,))
    
    def _search(self):
        """Search products and add to history."""
        keyword = self.search_var.get().strip()
        
        # Add to search history if not empty
        if keyword:
            self.search_history_manager.add_search(keyword)
            self._update_history_dropdown()
        
        self.current_page = 1
        self._load_products(keyword=keyword if keyword else None)
    
    def _clear_search(self):
        """Clear search and reload all products."""
        self.search_var.set("")
        self.history_var.set("")  # Clear history selection
        self.current_page = 1
        self._load_products()
    
    def _clear_history(self):
        """Clear search history."""
        self.search_history_manager.clear_history()
        self._update_history_dropdown()
        messagebox.showinfo("History Cleared", "Search history has been cleared.")
    
    def _on_history_selected(self, event=None):
        """Handle history selection from dropdown."""
        selected_history = self.history_var.get()
        if selected_history:
            # Set the search field to the selected history item
            self.search_var.set(selected_history)
            # Automatically perform the search
            self._search()
    
    def _update_history_dropdown(self):
        """Update the history dropdown with current search history."""
        history = self.search_history_manager.get_history()
        self.history_combo['values'] = history
        
        # Clear selection if current selection is not in history
        current_selection = self.history_var.get()
        if current_selection not in history:
            self.history_var.set("")
    
    def _list_all_stock(self):
        """List all stock from mock server (no keyword filter)."""
        self.search_var.set("")  # Clear search field
        self.current_page = 1
        self.status_var.set("Loading all stock from mock server...")
        self.window.update()
        
        try:
            # Load all products by searching with empty keyword
            result = self.api_client.search_products(
                keyword="",
                current_page=self.current_page,
                page_size=self.page_size
            )
            
            # Store LCSCProduct objects
            self.products = result.products
            total = result.total
            self.total_pages = result.total_pages
            
            self._populate_tree()
            
            self.result_count_var.set(f"📦 Total: {total:,} products in stock")
            self._update_pagination_info()
            self.status_var.set(f"✅ Listed all stock: Showing {len(self.products)} products (Page {self.current_page}/{self.total_pages}, Total: {total:,})")
            
            # Force UI update to ensure products are visible
            self.window.update_idletasks()
            
            logger.info(f"Listed all stock: {total} total products, showing page {self.current_page}/{self.total_pages}")
                
        except Exception as e:
            # Show error dialog (no modal grab needed)
            messagebox.showerror("Error", f"Failed to list all stock:\n{str(e)}")
            self.status_var.set("Error listing stock")
            logger.error(f"Failed to list all stock: {e}", exc_info=True)
    
    def _previous_page(self):
        """Go to previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            keyword = self.search_var.get().strip()
            self._load_products(keyword=keyword if keyword else None)
    
    def _next_page(self):
        """Go to next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            keyword = self.search_var.get().strip()
            self._load_products(keyword=keyword if keyword else None)
    
    def _first_page(self):
        """Go to first page."""
        if self.current_page > 1:
            self.current_page = 1
            keyword = self.search_var.get().strip()
            self._load_products(keyword=keyword if keyword else None)
    
    def _last_page(self):
        """Go to last page."""
        if self.current_page < self.total_pages:
            self.current_page = self.total_pages
            keyword = self.search_var.get().strip()
            self._load_products(keyword=keyword if keyword else None)
    
    def _change_page_size(self, event):
        """Change page size."""
        combo = event.widget
        new_page_size = int(combo.get())
        logger.info(f"Changing page size from {self.page_size} to {new_page_size}")
        self.page_size = new_page_size
        self.current_page = 1
        keyword = self.search_var.get().strip()
        self._load_products(keyword=keyword if keyword else None)
    
    def _create_page_buttons(self):
        """Create page number buttons for quick navigation."""
        # Clear existing buttons by destroying all children of the frame
        for widget in self.page_buttons_frame.winfo_children():
            widget.destroy()
        self.page_buttons.clear()
        
        if self.total_pages <= 1:
            return
        
        # Calculate which pages to show (max 5 buttons)
        max_buttons = 5
        
        # Calculate the range of pages to display
        half_range = max_buttons // 2  # 2 for max_buttons=5
        start_page = max(1, self.current_page - half_range)
        end_page = min(self.total_pages, self.current_page + half_range)
        
        # Adjust range to always show max_buttons if possible
        if end_page - start_page + 1 < max_buttons:
            if start_page == 1:
                # We're at the beginning, extend to the right
                end_page = min(self.total_pages, start_page + max_buttons - 1)
            elif end_page == self.total_pages:
                # We're at the end, extend to the left
                start_page = max(1, end_page - max_buttons + 1)
        
        # Debug logging
        logger.info(f"Creating page buttons: current={self.current_page}, total={self.total_pages}, range=[{start_page}-{end_page}]")
        
        # Create page buttons
        # Calculate button width based on total pages to prevent truncation
        button_width = len(str(self.total_pages))
        
        for page_num in range(start_page, end_page + 1):
            button_style = "Accent.TButton" if page_num == self.current_page else "TButton"
            
            # Use a closure with default parameter to capture the current page_num value
            def make_command(p):
                return lambda: self._go_to_page(p)
            
            button = ttk.Button(
                self.page_buttons_frame,
                text=str(page_num),
                command=make_command(page_num),
                style=button_style,
                width=button_width
            )
            button.pack(side=tk.LEFT, padx=1)
            self.page_buttons.append(button)
            logger.info(f"Created button for page {page_num}")
    
    def _go_to_page(self, page_num: int):
        """Go to a specific page number."""
        if 1 <= page_num <= self.total_pages and page_num != self.current_page:
            self.current_page = page_num
            keyword = self.search_var.get().strip()
            self._load_products(keyword=keyword if keyword else None)
    
    def _update_pagination_info(self):
        """Update pagination display after loading products."""
        self.page_info_var.set(f"Page {self.current_page} of {self.total_pages}")
        self._create_page_buttons()
    
    def _sort_by_column(self, column: str):
        """Sort the treeview by the specified column."""
        # Toggle sort direction if same column, otherwise default to ascending
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        
        # Get all items from tree
        items = [(self.tree.set(item, column), item) for item in self.tree.get_children('')]
        
        # Sort based on column type
        if column == "Stock":
            # Sort as integer - INVERTED to match price behavior
            # First click (↑) shows lowest stock, second click (↓) shows highest stock
            items.sort(key=lambda x: int(x[0]) if x[0].isdigit() else 0, reverse=not self.sort_reverse)
        elif column in ["Price (1+)", "Price (10+)", "Price (25+)", "Price (50+)", "Price (100+)", "Price (200+)", "Price (500+)", "Price (1000+)", "Price (5000+)", "Price (10000+)"]:
            # Sort as float (remove currency symbol and convert)
            def get_price(val):
                if not val or val == '':
                    return None  # Use None to handle empty separately
                try:
                    # Remove currency symbols except decimal point
                    import re
                    numeric_str = re.sub(r'[^\d.-]', '', val)
                    if numeric_str:
                        return float(numeric_str)
                    return None
                except (ValueError, TypeError):
                    return None
            
            # Separate items with prices from items without prices
            items_with_price = []
            items_without_price = []
            
            for val, item in items:
                price = get_price(val)
                if price is not None:
                    items_with_price.append((price, val, item))
                else:
                    items_without_price.append((val, item))
            
            # Sort items with prices
            # For prices: INVERT the sort direction
            # First click (sort_reverse=False) should show LOWEST prices first
            # Second click (sort_reverse=True) should show HIGHEST prices first
            items_with_price.sort(key=lambda x: x[0], reverse=not self.sort_reverse)
            
            # Combine: items with price first, then items without price (always at the end)
            items = [(x[1], x[2]) for x in items_with_price] + items_without_price
        else:
            # Sort as string
            items.sort(key=lambda x: x[0].lower(), reverse=self.sort_reverse)
        
        # Rearrange items in sorted positions
        for index, (val, item) in enumerate(items):
            self.tree.move(item, '', index)
        
        # Update column heading to show sort direction
        direction = " ↓" if self.sort_reverse else " ↑"
        columns = self.tree['columns']
        for col in columns:
            if col == column:
                self.tree.heading(col, text=f"{col}{direction}")
            elif col in ["Stock", "Price (1+)", "Price (10+)", "Price (100+)"]:
                # Reset other sortable columns
                self.tree.heading(col, text=col, command=lambda c=col: self._sort_by_column(c))
        
        self.status_var.set(f"Sorted by {column} ({'descending' if self.sort_reverse else 'ascending'})")
    
    def _show_details(self, event):
        """Show product details on double-click."""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.tree.item(item, 'values')
        
        if not values:
            return
        
        product_code = values[0]
        
        # Find product in list (LCSCProduct objects)
        product = None
        for p in self.products:
            if p.product_code == product_code:
                product = p
                break
        
        if not product:
            return
        
        # Create details window
        details_window = tk.Toplevel(self.window)
        details_window.title(f"Product Details - {product_code}")
        details_window.transient(self.window)
        
        # Apply theme to details window
        CorporateTheme.apply_to_toplevel(details_window)
        
        # Main frame (no scrollbar - will auto-size)
        main_frame = ttk.Frame(details_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Product details - fix Unicode encoding for Windows Tkinter
        description_text = product.description or 'N/A'
        # Replace Unicode characters with ASCII equivalents
        # Handle both proper Unicode and double-encoded characters
        description_text = (description_text
            .replace('Ω', 'ohm').replace('Î©', 'ohm')
            .replace('±', '+/-').replace('Â±', '+/-')
            .replace('µ', 'u').replace('Âµ', 'u')
            .replace('°', 'deg').replace('Â°', 'deg')
            .replace('≤', '<=').replace('â‰¤', '<=')
            .replace('≥', '>=').replace('â‰¥', '>=')
            .replace('Å', 'A')
            .replace('â€"', '-')
            .replace('Ã—', 'x')
        )
        # Remove any remaining non-ASCII characters
        description_text = description_text.encode('ascii', 'ignore').decode('ascii')
        
        details_text = f"""
Product Code: {product.product_code}
Product Number: {product.product_number}
Name: {product.product_name}
Manufacturer: {product.manufacturer}
MPN: {product.manufacturer_part}
Category: {product.category_name} (ID: {product.category_id})
Package: {product.package_type}
Stock: {product.stock}
Available: {'Yes' if product.is_available else 'No'}
Pre-sale: {'Yes' if product.is_pre_sale else 'No'}

=== Description ===
{description_text}

=== Pricing ===
"""
        
        for tier in product.price_tiers:
            details_text += f"{tier.quantity}+: ${tier.unit_price:.4f} {tier.currency}\n"
        
        # Remove the datasheet from text - we'll add it as an icon below
        # if product.datasheet_url:
        #     details_text += f"\n=== Links ===\nDatasheet: {product.datasheet_url}\n"
        
        # Show text details - calculate height based on content
        lines = details_text.strip().count('\n') + 1
        text_height = min(lines + 2, 30)  # Cap at 30 lines to prevent giant windows
        
        text_widget = tk.Text(main_frame, wrap=tk.WORD, padx=10, pady=10, width=70, height=text_height)
        text_widget.insert("1.0", details_text.strip())
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add PDF icon for datasheet if available
        if product.datasheet_url:
            datasheet_frame = ttk.Frame(main_frame)
            datasheet_frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(datasheet_frame, text="Datasheet:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
            
            # Create PDF icon button
            try:
                pdf_icon = self._create_pdf_icon(24)
                # Keep reference to prevent garbage collection
                details_window.pdf_icon = pdf_icon
                
                pdf_button = tk.Button(
                    datasheet_frame, 
                    image=pdf_icon, 
                    command=lambda: self._open_datasheet(product.datasheet_url),
                    relief=tk.FLAT,
                    bg=main_frame.cget('bg'),
                    activebackground=main_frame.cget('bg'),
                    borderwidth=0,
                    cursor='hand2'
                )
                pdf_button.pack(side=tk.LEFT, padx=(0, 10))
                
                # Add tooltip text
                url_label = ttk.Label(datasheet_frame, text="Click PDF icon to open datasheet", 
                                    foreground="#666", font=('Arial', 8))
                url_label.pack(side=tk.LEFT)
                
            except Exception as e:
                # Fallback to text link if icon creation fails
                link_label = ttk.Label(datasheet_frame, text=f"Open Datasheet", 
                                     foreground="blue", cursor="hand2")
                link_label.pack(side=tk.LEFT)
                link_label.bind("<Button-1>", lambda e: self._open_datasheet(product.datasheet_url))
        
        # Show image if available
        if product.image_url:
            image_frame = ttk.LabelFrame(main_frame, text="Component Image", padding="10")
            image_frame.pack(fill=tk.X, padx=10, pady=5)
            image_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Note: LCSC image URLs in mock data are not directly accessible
            # They would work with real API data or require web scraping
            info_text = (
                "Image URLs in mock data are not directly accessible.\n\n"
                f"Image URL:\n{product.image_url}\n\n"
                "Note: Real LCSC API returns working image URLs.\n"
                "Mock data uses placeholder URLs for testing."
            )
            ttk.Label(
                image_frame, 
                text=info_text,
                justify=tk.LEFT,
                wraplength=550,
                foreground="#666"
            ).pack(pady=5)
        
        # Close button
        ttk.Button(details_window, text="Close", command=details_window.destroy).pack(pady=10)
        
        # Update window to calculate size, then resize to fit content
        details_window.update_idletasks()
        details_window.geometry("")  # Auto-size to fit content
    
    def _create_pdf_icon(self, size=32):
        """Create a simple PDF icon using PIL."""
        # Create a simple PDF icon
        img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw PDF icon background (red rectangle)
        draw.rectangle([2, 2, size-2, size-2], fill='#DC143C', outline='#8B0000', width=2)
        
        # Draw "PDF" text (simplified)
        try:
            # Try to use a built-in font, fallback to default if not available
            from PIL import ImageFont
            try:
                font = ImageFont.truetype("arial.ttf", size//4)
            except:
                font = ImageFont.load_default()
            
            # Calculate text position to center it
            text = "PDF"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (size - text_width) // 2
            y = (size - text_height) // 2
            
            draw.text((x, y), text, fill='white', font=font)
        except:
            # Fallback: draw simple text
            draw.text((size//4, size//3), "PDF", fill='white')
        
        return ImageTk.PhotoImage(img)
    
    def _open_datasheet(self, url):
        """Open datasheet URL in the default web browser."""
        try:
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open datasheet:\n{str(e)}")
    
    def _export_csv(self):
        """Export products to CSV."""
        from tkinter import filedialog
        import csv
        from datetime import datetime
        
        if not self.products:
            messagebox.showwarning("No Data", "No products to export.")
            return
        
        # Ask for save location
        default_filename = f"mock_server_stock_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Header - include all 10 price break columns
                writer.writerow([
                    'Product Code', 'Product Number', 'Name', 'Manufacturer', 'MPN',
                    'Category', 'Package', 'Description', 'Stock', 'Available', 'Pre-sale',
                    'Price (1+)', 'Price (10+)', 'Price (25+)', 'Price (50+)', 'Price (100+)',
                    'Price (200+)', 'Price (500+)', 'Price (1000+)', 'Price (5000+)', 'Price (10000+)',
                    'Datasheet URL', 'Image URL'
                ])
                
                # Data (LCSCProduct objects)
                for product in self.products:
                    # Get prices from price tiers for all 10 possible quantities
                    price_breaks = {1: '', 10: '', 25: '', 50: '', 100: '', 200: '', 500: '', 1000: '', 5000: '', 10000: ''}
                    
                    for tier in product.price_tiers:
                        if tier.quantity in price_breaks:
                            price_breaks[tier.quantity] = f"{tier.unit_price:.4f}"
                    
                    # Clean description - fix Unicode encoding for CSV export
                    description_text = product.description or ''
                    description_text = (description_text
                        .replace('Ω', 'ohm').replace('Î©', 'ohm')
                        .replace('±', '+/-').replace('Â±', '+/-')
                        .replace('µ', 'u').replace('Âµ', 'u')
                        .replace('°', 'deg').replace('Â°', 'deg')
                        .replace('≤', '<=').replace('â‰¤', '<=')
                        .replace('≥', '>=').replace('â‰¥', '>=')
                        .replace('Å', 'A')
                        .replace('â€"', '-')
                        .replace('Ã—', 'x')
                    )
                    # Remove any remaining non-ASCII characters
                    description_text = description_text.encode('ascii', 'ignore').decode('ascii')
                    
                    writer.writerow([
                        product.product_code,
                        product.product_number,
                        product.product_name,
                        product.manufacturer,
                        product.manufacturer_part,
                        product.category_name,
                        product.package_type,
                        description_text,
                        product.stock,
                        'Yes' if product.is_available else 'No',
                        'Yes' if product.is_pre_sale else 'No',
                        price_breaks[1],
                        price_breaks[10],
                        price_breaks[25],
                        price_breaks[50],
                        price_breaks[100],
                        price_breaks[200],
                        price_breaks[500],
                        price_breaks[1000],
                        price_breaks[5000],
                        price_breaks[10000],
                        product.datasheet_url,
                        product.image_url
                    ])
            
            messagebox.showinfo("Export Successful", f"Exported {len(self.products)} products to:\n{filename}")
            self.status_var.set(f"Exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export CSV:\n{str(e)}")
            logger.error(f"Failed to export CSV: {e}", exc_info=True)

    def _minimize_window(self):
        """Minimize the window."""
        try:
            # Store current geometry if not already stored
            if not self.is_minimized and not self.is_fullscreen:
                self.normal_geometry = self.window.geometry()
            
            # No modal behavior to remove - just minimize
            # self.window.grab_release()
            # self.window.transient(None)
            
            # Minimize the window
            self.window.iconify()
            self.is_minimized = True
            
            # Bind to restore event
            self.window.bind('<Map>', self._on_restore)
            
        except Exception as e:
            logger.error(f"Failed to minimize window: {e}", exc_info=True)

    def _on_restore(self, event=None):
        """Handle window restore from minimize."""
        try:
            if self.is_minimized:
                self.is_minimized = False
                # Don't restore modal behavior - keep window interactive
                # self.window.transient(self.parent)
                # self.window.grab_set()
                # Unbind the restore event
                self.window.unbind('<Map>')
        except Exception as e:
            logger.error(f"Failed to restore window: {e}", exc_info=True)

    def _toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        try:
            if self.is_fullscreen:
                # Exit fullscreen
                self.window.attributes('-fullscreen', False)
                
                # Restore the exact geometry that was stored
                if self.normal_geometry:
                    self.window.geometry(self.normal_geometry)
                    # Show restoration info in status
                    self.status_var.set(f"✅ Restored geometry: {self.normal_geometry}")
                    # Schedule clearing the message after 3 seconds
                    self.window.after(3000, lambda: self.status_var.set("Ready"))
                    
                self.is_fullscreen = False
                
                # Don't restore modal behavior - keep window interactive for split screen
                # self.window.transient(self.parent) 
                # self.window.grab_set()
            else:
                # Enter fullscreen
                # Store current complete geometry (size + position)
                self.normal_geometry = self.window.geometry()
                # Show stored geometry in status
                self.status_var.set(f"Entering fullscreen. Stored geometry: {self.normal_geometry}")
                
                # Don't use modal behavior - keep window interactive
                # self.window.grab_release()
                # self.window.transient(None)
                
                # Set fullscreen
                self.window.attributes('-fullscreen', True)
                self.is_fullscreen = True
                
        except Exception as e:
            logger.error(f"Failed to toggle fullscreen: {e}", exc_info=True)
