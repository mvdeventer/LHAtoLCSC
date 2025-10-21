"""
Stock Browser Window - Debug tool for viewing mock server inventory.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Optional

from lhatolcsc.api.client import LCSCClient
from lhatolcsc.core.config import Config

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
        self.page_size = 100
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title(f"Stock Browser (Debug) - {config.app_name} v{config.version}")
        self.window.geometry("1200x700")
        self.window.minsize(1000, 600)
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
        self._create_widgets()
        self._load_products()
    
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
            font=("Segoe UI", 14, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Info label
        info_label = ttk.Label(
            main_frame,
            text="Browse components available in the mock server. Use search to filter results.",
            foreground="gray"
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
        
        search_button = ttk.Button(search_frame, text="Search", command=self._search)
        search_button.grid(row=0, column=2, padx=5)
        
        clear_button = ttk.Button(search_frame, text="Clear", command=self._clear_search)
        clear_button.grid(row=0, column=3, padx=5)
        
        self.result_count_var = tk.StringVar(value="No products loaded")
        result_label = ttk.Label(search_frame, textvariable=self.result_count_var, foreground="blue")
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
        
        # Treeview
        columns = (
            "Product Code",
            "Model",
            "Name",
            "Brand",
            "Package",
            "Stock",
            "Price (1+)",
            "Price (10+)",
            "Price (100+)"
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
        self.tree.column("Model", width=120, anchor="w")
        self.tree.column("Name", width=300, anchor="w")
        self.tree.column("Brand", width=120, anchor="w")
        self.tree.column("Package", width=80, anchor="center")
        self.tree.column("Stock", width=80, anchor="e")
        self.tree.column("Price (1+)", width=80, anchor="e")
        self.tree.column("Price (10+)", width=80, anchor="e")
        self.tree.column("Price (100+)", width=80, anchor="e")
        
        # Configure headings
        for col in columns:
            self.tree.heading(col, text=col, anchor="w" if col in ["Name", "Model"] else "center")
        
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
            values=["50", "100", "200", "500"],
            width=10,
            state="readonly"
        )
        page_size_combo.set(self.page_size)
        page_size_combo.bind('<<ComboboxSelected>>', self._change_page_size)
        page_size_combo.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            foreground="blue"
        )
        status_bar.grid(row=5, column=0, columnspan=3, sticky="ew")
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(button_frame, text="List All Stock", command=self._list_all_stock).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self._load_products).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to CSV", command=self._export_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=self.window.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
    
    def _load_products(self, keyword: Optional[str] = None):
        """Load products from API."""
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
    
    def _populate_tree(self):
        """Populate treeview with products."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add products (LCSCProduct objects)
        for product in self.products:
            product_code = product.product_code or 'N/A'
            model = product.manufacturer_part or 'N/A'
            name = product.product_name or 'N/A'
            brand = product.manufacturer or 'N/A'
            package = product.package_type or 'N/A'
            stock = str(product.stock)
            
            # Get prices from price tiers
            price_1 = price_10 = price_100 = 'N/A'
            
            for tier in product.price_tiers:
                if tier.quantity == 1:
                    price_1 = f"${tier.unit_price:.4f}"
                elif tier.quantity == 10:
                    price_10 = f"${tier.unit_price:.4f}"
                elif tier.quantity == 100:
                    price_100 = f"${tier.unit_price:.4f}"
            
            values = (
                product_code,
                model,
                name,
                brand,
                package,
                stock,
                price_1,
                price_10,
                price_100
            )
            
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
        self.page_size = int(combo.get())
        self.current_page = 1
        keyword = self.search_var.get().strip()
        self._load_products(keyword=keyword if keyword else None)
    
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
        details_window.geometry("600x500")
        details_window.transient(self.window)
        
        # Main frame with scrollbar
        canvas = tk.Canvas(details_window)
        scrollbar = ttk.Scrollbar(details_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Product details
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
{product.description or 'N/A'}

=== Pricing ===
"""
        
        for tier in product.price_tiers:
            details_text += f"{tier.quantity}+: ${tier.unit_price:.4f} {tier.currency}\n"
        
        if product.datasheet_url:
            details_text += f"\n=== Links ===\nDatasheet: {product.datasheet_url}\n"
        
        if product.image_url:
            details_text += f"Image: {product.image_url}\n"
        
        text_widget = tk.Text(scrollable_frame, wrap=tk.WORD, padx=10, pady=10, width=60, height=25)
        text_widget.insert("1.0", details_text.strip())
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Close button
        ttk.Button(details_window, text="Close", command=details_window.destroy).pack(pady=10)
    
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
                
                # Header
                writer.writerow([
                    'Product Code', 'Product Number', 'Name', 'Manufacturer', 'MPN',
                    'Category', 'Package', 'Stock', 'Available', 'Pre-sale',
                    'Price (1+)', 'Price (10+)', 'Price (100+)', 'Datasheet URL'
                ])
                
                # Data (LCSCProduct objects)
                for product in self.products:
                    # Get prices from price tiers
                    price_1 = price_10 = price_100 = ''
                    
                    for tier in product.price_tiers:
                        if tier.quantity == 1:
                            price_1 = f"{tier.unit_price:.4f}"
                        elif tier.quantity == 10:
                            price_10 = f"{tier.unit_price:.4f}"
                        elif tier.quantity == 100:
                            price_100 = f"{tier.unit_price:.4f}"
                    
                    writer.writerow([
                        product.product_code,
                        product.product_number,
                        product.product_name,
                        product.manufacturer,
                        product.manufacturer_part,
                        product.category_name,
                        product.package_type,
                        product.stock,
                        'Yes' if product.is_available else 'No',
                        'Yes' if product.is_pre_sale else 'No',
                        price_1,
                        price_10,
                        price_100,
                        product.datasheet_url
                    ])
            
            messagebox.showinfo("Export Successful", f"Exported {len(self.products)} products to:\n{filename}")
            self.status_var.set(f"Exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export CSV:\n{str(e)}")
            logger.error(f"Failed to export CSV: {e}", exc_info=True)
