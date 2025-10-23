"""
Stock Browser Window - Debug tool for viewing mock server inventory.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Optional
from io import BytesIO
import requests
from PIL import Image, ImageTk

from lhatolcsc.api.client import LCSCClient
from lhatolcsc.core.config import Config
from lhatolcsc.gui.theme import CorporateTheme

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
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title(f"Stock Browser (Debug) - {config.app_name} v{config.version}")
        self.window.geometry("2200x700")  # Wider to fit 10 price columns
        self.window.minsize(1800, 600)
        
        # Apply corporate theme
        CorporateTheme.apply_to_toplevel(self.window)
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
        self._create_widgets()
        # Don't auto-load products - wait for user to search
        self.status_var.set("Ready. Enter search term or click 'List All' to load products.")
    
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
        
        ttk.Label(search_frame, text="Keyword:").grid(row=0, column=0, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.grid(row=0, column=1, padx=5, sticky="ew")
        search_entry.bind('<Return>', lambda e: self._search())
        
        search_button = ttk.Button(search_frame, text="Search", command=self._search, style="Accent.TButton")
        search_button.grid(row=0, column=2, padx=5)
        
        clear_button = ttk.Button(search_frame, text="Clear", command=self._clear_search)
        clear_button.grid(row=0, column=3, padx=5)
        
        self.result_count_var = tk.StringVar(value="No products loaded")
        result_label = ttk.Label(search_frame, textvariable=self.result_count_var)
        result_label.grid(row=0, column=4, padx=10)
        
        search_frame.columnconfigure(1, weight=1)
        
        # Treeview frame
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(0, 10))
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Define columns - ALL 10 possible price breaks (no image column for speed)
        columns = (
            "Product Code",
            "Model",
            "Brand",
            "Category",
            "Package",
            "Description",
            "Stock",
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
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="tree headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            selectmode="browse"
        )
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.column("#0", width=0, stretch=False)
        self.tree.column("Product Code", width=100, anchor="w")
        self.tree.column("Model", width=150, anchor="w")
        self.tree.column("Brand", width=120, anchor="w")
        self.tree.column("Category", width=120, anchor="w")
        self.tree.column("Package", width=80, anchor="center")
        self.tree.column("Description", width=300, anchor="w")
        self.tree.column("Stock", width=80, anchor="e")
        self.tree.column("Price (1+)", width=75, anchor="e")
        self.tree.column("Price (10+)", width=75, anchor="e")
        self.tree.column("Price (25+)", width=75, anchor="e")
        self.tree.column("Price (50+)", width=75, anchor="e")
        self.tree.column("Price (100+)", width=80, anchor="e")
        self.tree.column("Price (200+)", width=80, anchor="e")
        self.tree.column("Price (500+)", width=80, anchor="e")
        self.tree.column("Price (1000+)", width=85, anchor="e")
        self.tree.column("Price (5000+)", width=85, anchor="e")
        self.tree.column("Price (10000+)", width=85, anchor="e")
        
        # Configure headings with sorting
        for col in columns:
            if col in ["Model", "Description"]:
                self.tree.heading(col, text=col, anchor="w")
            elif col in ["Stock", "Price (1+)", "Price (10+)", "Price (25+)", "Price (50+)", "Price (100+)", "Price (200+)", "Price (500+)", "Price (1000+)", "Price (5000+)", "Price (10000+)"]:
                # Add sorting to stock and price columns
                self.tree.heading(col, text=col, anchor="center", 
                                command=lambda c=col: self._sort_by_column(c))
            else:
                self.tree.heading(col, text=col, anchor="center")
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind double-click to show details
        self.tree.bind('<Double-Button-1>', self._show_details)
        
        # Pagination frame
        pagination_frame = ttk.Frame(main_frame)
        pagination_frame.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        
        self.page_info_var = tk.StringVar(value="Page 1 of 1")
        ttk.Label(pagination_frame, textvariable=self.page_info_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(pagination_frame, text="◀ Previous", command=self._previous_page).pack(side=tk.LEFT, padx=5)
        ttk.Button(pagination_frame, text="Next ▶", command=self._next_page).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(pagination_frame, text="Page size:").pack(side=tk.LEFT, padx=(20, 5))
        page_size_combo = ttk.Combobox(
            pagination_frame,
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
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(button_frame, text="List All Stock", command=self._list_all_stock, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self._load_products).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to CSV", command=self._export_csv, style="Success.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=self.window.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
    
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
            self.page_info_var.set(f"Page {self.current_page} of {self.total_pages}")
            self.status_var.set(f"Loaded {len(self.products)} products (Page {self.current_page}/{self.total_pages})")
            
            # Force UI update
            self.window.update_idletasks()
            
            logger.info(f"Loaded {len(self.products)} products from mock server")
                
        except Exception as e:
            # Temporarily release grab for error dialog
            self.window.grab_release()
            messagebox.showerror("Error", f"Failed to load products:\n{str(e)}")
            self.window.grab_set()
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
            
            # Get prices from ALL 10 price tiers - show empty if not available
            price_dict = {tier.quantity: tier.unit_price for tier in product.price_tiers}
            
            price_1 = f"${price_dict.get(1, 0):.4f}" if 1 in price_dict else ''
            price_10 = f"${price_dict.get(10, 0):.4f}" if 10 in price_dict else ''
            price_25 = f"${price_dict.get(25, 0):.4f}" if 25 in price_dict else ''
            price_50 = f"${price_dict.get(50, 0):.4f}" if 50 in price_dict else ''
            price_100 = f"${price_dict.get(100, 0):.4f}" if 100 in price_dict else ''
            price_200 = f"${price_dict.get(200, 0):.4f}" if 200 in price_dict else ''
            price_500 = f"${price_dict.get(500, 0):.4f}" if 500 in price_dict else ''
            price_1000 = f"${price_dict.get(1000, 0):.4f}" if 1000 in price_dict else ''
            price_5000 = f"${price_dict.get(5000, 0):.4f}" if 5000 in price_dict else ''
            price_10000 = f"${price_dict.get(10000, 0):.4f}" if 10000 in price_dict else ''
            
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
        """Search products."""
        keyword = self.search_var.get().strip()
        self.current_page = 1
        self._load_products(keyword=keyword if keyword else None)
    
    def _clear_search(self):
        """Clear search and reload all products."""
        self.search_var.set("")
        self.current_page = 1
        self._load_products()
    
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
            self.page_info_var.set(f"Page {self.current_page} of {self.total_pages}")
            self.status_var.set(f"✅ Listed all stock: Showing {len(self.products)} products (Page {self.current_page}/{self.total_pages}, Total: {total:,})")
            
            # Force UI update to ensure products are visible
            self.window.update_idletasks()
            
            logger.info(f"Listed all stock: {total} total products, showing page {self.current_page}/{self.total_pages}")
                
        except Exception as e:
            # Temporarily release grab for error dialog
            self.window.grab_release()
            messagebox.showerror("Error", f"Failed to list all stock:\n{str(e)}")
            self.window.grab_set()
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
    
    def _change_page_size(self, event):
        """Change page size."""
        combo = event.widget
        new_page_size = int(combo.get())
        logger.info(f"Changing page size from {self.page_size} to {new_page_size}")
        self.page_size = new_page_size
        self.current_page = 1
        keyword = self.search_var.get().strip()
        self._load_products(keyword=keyword if keyword else None)
    
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
            # Sort as float (remove $ and convert)
            def get_price(val):
                if not val or val == '':
                    return None  # Use None to handle empty separately
                try:
                    return float(val.replace('$', ''))
                except:
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
        
        if product.datasheet_url:
            details_text += f"\n=== Links ===\nDatasheet: {product.datasheet_url}\n"
        
        # Show text details - calculate height based on content
        lines = details_text.strip().count('\n') + 1
        text_height = min(lines + 2, 30)  # Cap at 30 lines to prevent giant windows
        
        text_widget = tk.Text(main_frame, wrap=tk.WORD, padx=10, pady=10, width=70, height=text_height)
        text_widget.insert("1.0", details_text.strip())
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
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
