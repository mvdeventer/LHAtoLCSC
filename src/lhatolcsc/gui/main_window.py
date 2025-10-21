"""
Main application window.
"""

import logging
import tkinter as tk
from tkinter import ttk, messagebox

from lhatolcsc.api.client import LCSCClient
from lhatolcsc.core.config import Config
from lhatolcsc.gui.settings_dialog import SettingsDialog


logger = logging.getLogger(__name__)


class MainWindow:
    """Main application window."""
    
    def __init__(self, root: tk.Tk, config: Config):
        """
        Initialize main window.
        
        Args:
            root: Tkinter root window
            config: Application configuration
        """
        self.root = root
        self.config = config
        self.api_client: LCSCClient | None = None
        
        # Setup window
        self.root.title(f"{config.app_name} v{config.version}")
        self.root.geometry(f"{config.window_width}x{config.window_height}")
        
        # Setup API client if configured
        if config.is_configured():
            try:
                self.api_client = LCSCClient(
                    api_key=config.lcsc_api_key,
                    api_secret=config.lcsc_api_secret,
                    base_url=config.lcsc_api_url,
                    timeout=config.request_timeout
                )
                logger.info("API client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize API client: {e}")
                messagebox.showerror("API Error", f"Failed to initialize API client:\n{e}")
        
        self._create_widgets()
        logger.info("Application GUI initialized")
    
    def _create_widgets(self) -> None:
        """Create GUI widgets."""
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load BOM...", command=self._load_bom)
        file_menu.add_command(label="Export BOM...", command=self._export_bom)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Settings...", command=self._show_settings)
        tools_menu.add_command(label="Test API Connection", command=self._test_api)
        tools_menu.add_separator()
        tools_menu.add_command(label="Reset Credentials...", command=self._reset_credentials)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Guide", command=self._show_help)
        help_menu.add_command(label="About", command=self._show_about)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Welcome label
        welcome_label = ttk.Label(
            main_frame,
            text=f"Welcome to {self.config.app_name}",
            font=("Arial", 16, "bold")
        )
        welcome_label.grid(row=0, column=0, pady=20)
        
        # Instructions
        instructions = (
            "1. Load your BOM Excel file\n"
            "2. Map the 'Stock Part Name' column\n"
            "3. Click 'Start Matching' to find LCSC parts\n"
            "4. Review and approve matches\n"
            "5. Export enhanced BOM with LCSC part numbers"
        )
        instructions_label = ttk.Label(main_frame, text=instructions, justify=tk.LEFT)
        instructions_label.grid(row=1, column=0, pady=10)
        
        # Load BOM button
        load_button = ttk.Button(
            main_frame,
            text="Load BOM File",
            command=self._load_bom,
            width=30
        )
        load_button.grid(row=2, column=0, pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
    
    def _load_bom(self) -> None:
        """Load BOM file."""
        messagebox.showinfo("Coming Soon", "BOM loading feature coming soon!")
    
    def _export_bom(self) -> None:
        """Export enhanced BOM."""
        messagebox.showinfo("Coming Soon", "BOM export feature coming soon!")
    
    def _show_settings(self) -> None:
        """Show settings dialog."""
        dialog = SettingsDialog(self.root, self.config, is_first_run=False)
        if dialog.show():
            # Reinitialize API client with new settings
            if self.config.is_configured():
                try:
                    self.api_client = LCSCClient(
                        api_key=self.config.lcsc_api_key,
                        api_secret=self.config.lcsc_api_secret,
                        base_url=self.config.lcsc_api_url,
                        timeout=self.config.request_timeout
                    )
                    self.status_var.set("Settings updated and API client reinitialized")
                    logger.info("API client reinitialized after settings update")
                except Exception as e:
                    logger.error(f"Failed to reinitialize API client: {e}")
                    messagebox.showerror("API Error", f"Failed to initialize API client:\n{e}")
    
    def _test_api(self) -> None:
        """Test API connection."""
        if not self.api_client:
            messagebox.showwarning(
                "API Not Configured",
                "Please configure your LCSC API credentials in the .env file."
            )
            return
        
        self.status_var.set("Testing API connection...")
        self.root.update()
        
        if self.api_client.test_connection():
            messagebox.showinfo("Success", "API connection successful!")
            self.status_var.set("API connection successful")
        else:
            messagebox.showerror("Error", "API connection failed!")
            self.status_var.set("API connection failed")
    
    def _reset_credentials(self) -> None:
        """Reset API credentials - clears .env file and shows setup wizard on next restart."""
        from pathlib import Path
        
        # Confirm action
        response = messagebox.askyesno(
            "Reset Credentials",
            "This will clear your API credentials and settings.\n\n"
            "The setup wizard will appear when you restart the application.\n\n"
            "Do you want to continue?",
            icon=messagebox.WARNING
        )
        
        if not response:
            return
        
        try:
            env_path = Path(self.config.project_root) / ".env"
            
            if env_path.exists():
                # Backup existing .env file
                backup_path = env_path.with_suffix(".env.backup")
                import shutil
                shutil.copy2(env_path, backup_path)
                logger.info(f"Backed up .env to {backup_path}")
                
                # Clear the .env file (write minimal content)
                with open(env_path, "w") as f:
                    f.write("# LHAtoLCSC Configuration\n")
                    f.write("# Credentials have been reset\n")
                    f.write("# The setup wizard will appear on next startup\n\n")
                    f.write("LCSC_API_KEY=\n")
                    f.write("LCSC_API_SECRET=\n")
                
                logger.info("Credentials reset successfully")
                
                messagebox.showinfo(
                    "Credentials Reset",
                    "Credentials have been cleared successfully!\n\n"
                    f"A backup has been saved to:\n{backup_path}\n\n"
                    "The setup wizard will appear when you restart the application.\n\n"
                    "Click OK to close the application."
                )
                
                # Close the application
                self.root.quit()
            else:
                messagebox.showinfo(
                    "No Configuration Found",
                    "No configuration file found. The setup wizard will appear automatically on next startup."
                )
        except Exception as e:
            logger.error(f"Failed to reset credentials: {e}")
            messagebox.showerror(
                "Reset Failed",
                f"Failed to reset credentials:\n{str(e)}\n\n"
                "Please manually delete or edit the .env file."
            )
    
    def _show_help(self) -> None:
        """Show user guide."""
        messagebox.showinfo("Coming Soon", "User guide coming soon!")
    
    def _show_about(self) -> None:
        """Show about dialog."""
        about_text = (
            f"{self.config.app_name} v{self.config.version}\n\n"
            "BOM to LCSC Part Matcher\n\n"
            "A professional desktop application for matching\n"
            "Bill of Materials components with LCSC parts\n"
            "using intelligent fuzzy search.\n\n"
            "© 2025 - MIT License"
        )
        messagebox.showinfo("About", about_text)
