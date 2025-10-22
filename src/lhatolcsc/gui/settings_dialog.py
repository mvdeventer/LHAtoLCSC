"""
Settings dialog for LHAtoLCSC application.

Allows users to configure API credentials and other settings.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from typing import Optional
import logging

from ..core.config import Config
from .theme import CorporateTheme

logger = logging.getLogger(__name__)


class SettingsDialog:
    """Dialog for configuring application settings."""

    def __init__(self, parent: Optional[tk.Tk], config: Config, is_first_run: bool = False):
        """
        Initialize the settings dialog.

        Args:
            parent: Parent window (None for standalone mode)
            config: Application configuration
            is_first_run: Whether this is the first time running the app
        """
        self.config = config
        self.is_first_run = is_first_run
        self.result: Optional[bool] = None
        
        # If no parent, create main window; otherwise create dialog
        if parent is None:
            # Standalone mode - create as main Tk window
            self.window = tk.Tk()
            self.standalone = True
            # Apply theme to root window
            CorporateTheme.apply_to_root(self.window)
        else:
            # Dialog mode - create as Toplevel
            self.window = tk.Toplevel(parent)
            self.standalone = False
            self.window.transient(parent)
            # Apply theme to toplevel window
            CorporateTheme.apply_to_toplevel(self.window)
        
        # Configure window
        title_suffix = " - First Time Setup" if is_first_run else " - Settings"
        self.window.title(f"{config.app_name} v{config.version}{title_suffix}")
        self.window.geometry("650x700")
        self.window.resizable(True, True)
        self.window.minsize(650, 700)
        
        # Make dialog modal
        self.window.grab_set()

        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (650 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"650x700+{x}+{y}")
        
        # Make sure window is visible
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()

        self._create_widgets()
        self._load_current_settings()

        # Bind close button
        self.window.protocol("WM_DELETE_WINDOW", self._on_cancel)

        # Focus on first entry
        self.api_key_entry.focus()

    def _create_widgets(self):
        """Create dialog widgets."""
        # Main frame with padding
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        # Title label for first run
        if self.is_first_run:
            title_label = ttk.Label(
                main_frame,
                text="Welcome to LHAtoLCSC!",
                style="Title.TLabel"
            )
            title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

            info_label = ttk.Label(
                main_frame,
                text="Please configure your LCSC API credentials to get started.",
                wraplength=550
            )
            info_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
            start_row = 2
        else:
            start_row = 0

        # API Settings Section
        api_label = ttk.Label(main_frame, text="LCSC API Settings", style="Header.TLabel")
        api_label.grid(row=start_row, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        # API Key
        ttk.Label(main_frame, text="API Key:").grid(row=start_row + 1, column=0, sticky=tk.W, pady=5)
        self.api_key_entry = ttk.Entry(main_frame, width=50)
        self.api_key_entry.grid(row=start_row + 1, column=1, sticky="ew", pady=5)

        # API Secret
        ttk.Label(main_frame, text="API Secret:").grid(row=start_row + 2, column=0, sticky=tk.W, pady=5)
        self.api_secret_entry = ttk.Entry(main_frame, width=50, show="*")
        self.api_secret_entry.grid(row=start_row + 2, column=1, sticky="ew", pady=5)

        # Show/Hide secret button
        self.show_secret_var = tk.BooleanVar(value=False)
        show_secret_check = ttk.Checkbutton(
            main_frame,
            text="Show API Secret",
            variable=self.show_secret_var,
            command=self._toggle_secret_visibility
        )
        show_secret_check.grid(row=start_row + 3, column=1, sticky=tk.W, pady=5)

        # API Base URL
        ttk.Label(main_frame, text="API Base URL:").grid(row=start_row + 4, column=0, sticky=tk.W, pady=5)
        self.api_url_entry = ttk.Entry(main_frame, width=50)
        self.api_url_entry.grid(row=start_row + 4, column=1, sticky="ew", pady=5)

        # Mock Server Button
        mock_server_button = ttk.Button(
            main_frame,
            text="🧪 Use Mock Server Credentials",
            command=self._fill_mock_credentials
        )
        mock_server_button.grid(row=start_row + 5, column=1, sticky=tk.W, pady=5)

        # Network Settings Section
        network_label = ttk.Label(
            main_frame,
            text="Network Settings",
            style="Header.TLabel"
        )
        network_label.grid(row=start_row + 6, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))

        # IP Address (for whitelisting reference)
        ttk.Label(main_frame, text="Your IP Address:").grid(row=start_row + 7, column=0, sticky=tk.W, pady=5)
        self.ip_entry = ttk.Entry(main_frame, width=50)
        self.ip_entry.grid(row=start_row + 7, column=1, sticky="ew", pady=5)

        # Get IP button
        get_ip_button = ttk.Button(
            main_frame,
            text="Detect My IP",
            command=self._detect_ip
        )
        get_ip_button.grid(row=start_row + 8, column=1, sticky=tk.W, pady=5)

        # Timeout
        ttk.Label(main_frame, text="Request Timeout (s):").grid(row=start_row + 9, column=0, sticky=tk.W, pady=5)
        self.timeout_var = tk.IntVar(value=30)
        timeout_spinbox = ttk.Spinbox(
            main_frame,
            from_=5,
            to=120,
            textvariable=self.timeout_var,
            width=10
        )
        timeout_spinbox.grid(row=start_row + 9, column=1, sticky=tk.W, pady=5)

        # Application Settings Section
        app_label = ttk.Label(
            main_frame,
            text="Application Settings",
            style="Header.TLabel"
        )
        app_label.grid(row=start_row + 10, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))

        # Default match threshold
        ttk.Label(main_frame, text="Match Threshold (%):").grid(row=start_row + 11, column=0, sticky=tk.W, pady=5)
        self.threshold_var = tk.IntVar(value=70)
        threshold_spinbox = ttk.Spinbox(
            main_frame,
            from_=0,
            to=100,
            textvariable=self.threshold_var,
            width=10
        )
        threshold_spinbox.grid(row=start_row + 11, column=1, sticky=tk.W, pady=5)

        # Info label
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=start_row + 12, column=0, columnspan=2, pady=(20, 10), sticky="ew")

        info_text = ttk.Label(
            info_frame,
            text="Note: To get API credentials, visit https://www.lcsc.com/agent\n"
                 "and apply for API access. You'll need to whitelist your IP address.",
            wraplength=550,
            justify=tk.LEFT
        )
        info_text.pack(side=tk.LEFT)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=start_row + 13, column=0, columnspan=2, pady=(20, 0), sticky=(tk.E))

        # Save button
        save_button = ttk.Button(
            button_frame,
            text="Save" if not self.is_first_run else "Save & Continue",
            command=self._on_save,
            style="Success.TButton",
            width=15
        )
        save_button.pack(side=tk.RIGHT, padx=5)

        # Cancel button (not shown on first run if no credentials)
        if not self.is_first_run or self.config.lcsc_api_key:
            cancel_button = ttk.Button(
                button_frame,
                text="Cancel",
                command=self._on_cancel,
                width=15
            )
            cancel_button.pack(side=tk.RIGHT, padx=5)

        # Test Connection button
        test_button = ttk.Button(
            button_frame,
            text="Test Connection",
            command=self._test_connection,
            style="Accent.TButton",
            width=15
        )
        test_button.pack(side=tk.RIGHT, padx=5)

        # Version footer
        version_frame = ttk.Frame(main_frame)
        version_frame.grid(row=start_row + 14, column=0, columnspan=2, pady=(10, 0))
        
        version_label = ttk.Label(
            version_frame,
            text=f"v{self.config.version}"
        )
        version_label.pack()

        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)

    def _toggle_secret_visibility(self):
        """Toggle visibility of API secret."""
        if self.show_secret_var.get():
            self.api_secret_entry.configure(show="")
        else:
            self.api_secret_entry.configure(show="*")

    def _fill_mock_credentials(self):
        """Fill in the mock server credentials for testing."""
        # Clear existing entries
        self.api_key_entry.delete(0, tk.END)
        self.api_secret_entry.delete(0, tk.END)
        self.api_url_entry.delete(0, tk.END)
        
        # Fill with mock server credentials
        self.api_key_entry.insert(0, "test_api_key_12345")
        self.api_secret_entry.insert(0, "test_api_secret_67890")
        self.api_url_entry.insert(0, "http://localhost:5000")
        
        messagebox.showinfo(
            "Mock Server Credentials",
            "Mock server credentials have been filled in!\n\n"
            "These credentials work with the mock LCSC API server.\n\n"
            "Make sure the mock server is running:\n"
            "  python tests/mock_lcsc_server.py\n\n"
            "Mock Database: 104,042+ components\n"
            "  • 35,280 Resistors\n"
            "  • 49,329 Capacitors\n"
            "  • 8,652 Inductors\n"
            "  • 6,780 Crystals\n"
            "  • 1,305 ICs\n"
            "  • 516 Sensors\n"
            "  • 2,180 Connectors"
        )

    def _load_current_settings(self):
        """Load current settings from config."""
        # Load API settings
        if self.config.lcsc_api_key:
            self.api_key_entry.insert(0, self.config.lcsc_api_key)
        
        if self.config.lcsc_api_secret:
            self.api_secret_entry.insert(0, self.config.lcsc_api_secret)
        
        if self.config.lcsc_api_url:
            self.api_url_entry.insert(0, self.config.lcsc_api_url)
        else:
            self.api_url_entry.insert(0, "https://api.lcsc.com/v1")

        # Load network settings
        if hasattr(self.config, 'user_ip') and self.config.user_ip:
            self.ip_entry.insert(0, self.config.user_ip)
        
        # Load timeout
        if hasattr(self.config, 'request_timeout'):
            self.timeout_var.set(self.config.request_timeout)
        
        # Load match threshold
        if hasattr(self.config, 'default_match_threshold'):
            self.threshold_var.set(int(self.config.default_match_threshold * 100))

    def _detect_ip(self):
        """Detect and display the user's public IP address."""
        try:
            import requests
            response = requests.get("https://api.ipify.org?format=json", timeout=5)
            response.raise_for_status()
            ip_address = response.json().get("ip", "")
            
            if ip_address:
                self.ip_entry.delete(0, tk.END)
                self.ip_entry.insert(0, ip_address)
                messagebox.showinfo(
                    "IP Detected",
                    f"Your public IP address is: {ip_address}\n\n"
                    "Make sure to whitelist this IP in your LCSC API settings."
                )
            else:
                messagebox.showwarning("IP Detection", "Could not detect IP address.")
        except Exception as e:
            logger.error(f"Failed to detect IP: {e}")
            messagebox.showerror(
                "Error",
                f"Failed to detect IP address:\n{str(e)}\n\n"
                "You can manually enter your IP or check online."
            )

    def _test_connection(self):
        """Test the API connection with current settings."""
        api_key = self.api_key_entry.get().strip()
        api_secret = self.api_secret_entry.get().strip()
        api_url = self.api_url_entry.get().strip()

        if not api_key or not api_secret:
            messagebox.showwarning(
                "Missing Credentials",
                "Please enter both API Key and API Secret to test the connection."
            )
            return

        try:
            from ..api.client import LCSCClient

            # Create temporary client
            client = LCSCClient(
                api_key=api_key,
                api_secret=api_secret,
                base_url=api_url,
                timeout=self.timeout_var.get()
            )

            # Test connection
            if client.test_connection():
                messagebox.showinfo(
                    "Connection Successful",
                    "Successfully connected to LCSC API!\n\n"
                    "Your credentials are working correctly."
                )
            else:
                messagebox.showerror(
                    "Connection Failed",
                    "Failed to connect to LCSC API.\n\n"
                    "Please check your credentials and network connection."
                )
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            messagebox.showerror(
                "Connection Error",
                f"Failed to test connection:\n{str(e)}\n\n"
                "Please check your credentials and try again."
            )

    def _validate_settings(self) -> bool:
        """Validate all settings before saving."""
        api_key = self.api_key_entry.get().strip()
        api_secret = self.api_secret_entry.get().strip()
        api_url = self.api_url_entry.get().strip()

        # API credentials are required
        if not api_key:
            messagebox.showwarning("Validation Error", "API Key is required.")
            self.api_key_entry.focus()
            return False

        if not api_secret:
            messagebox.showwarning("Validation Error", "API Secret is required.")
            self.api_secret_entry.focus()
            return False

        if not api_url:
            messagebox.showwarning("Validation Error", "API Base URL is required.")
            self.api_url_entry.focus()
            return False

        # Validate URL format
        if not api_url.startswith(("http://", "https://")):
            messagebox.showwarning(
                "Validation Error",
                "API Base URL must start with http:// or https://"
            )
            self.api_url_entry.focus()
            return False

        return True

    def _save_settings(self):
        """Save settings to .env file."""
        try:
            env_path = Path(self.config.project_root) / ".env"
            
            # Read existing .env file if it exists
            env_content = {}
            if env_path.exists():
                with open(env_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            env_content[key.strip()] = value.strip()

            # Update with new values
            env_content["LCSC_API_KEY"] = self.api_key_entry.get().strip()
            env_content["LCSC_API_SECRET"] = self.api_secret_entry.get().strip()
            env_content["LCSC_API_URL"] = self.api_url_entry.get().strip()
            env_content["USER_IP"] = self.ip_entry.get().strip()
            env_content["REQUEST_TIMEOUT"] = str(self.timeout_var.get())
            env_content["DEFAULT_MATCH_THRESHOLD"] = str(self.threshold_var.get() / 100)

            # Write back to .env file
            with open(env_path, "w") as f:
                f.write("# LHAtoLCSC Configuration\n")
                f.write("# Generated by Settings Dialog\n\n")
                f.write("# LCSC API Credentials\n")
                f.write(f"LCSC_API_KEY={env_content['LCSC_API_KEY']}\n")
                f.write(f"LCSC_API_SECRET={env_content['LCSC_API_SECRET']}\n")
                f.write(f"LCSC_API_URL={env_content['LCSC_API_URL']}\n\n")
                f.write("# Network Settings\n")
                f.write(f"USER_IP={env_content['USER_IP']}\n")
                f.write(f"REQUEST_TIMEOUT={env_content['REQUEST_TIMEOUT']}\n\n")
                f.write("# Application Settings\n")
                f.write(f"DEFAULT_MATCH_THRESHOLD={env_content['DEFAULT_MATCH_THRESHOLD']}\n")

            logger.info(f"Settings saved to {env_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            messagebox.showerror(
                "Save Error",
                f"Failed to save settings:\n{str(e)}"
            )
            return False

    def _on_save(self):
        """Handle save button click."""
        if not self._validate_settings():
            return

        if self._save_settings():
            # Reload config to apply changes
            self.config.reload()
            
            messagebox.showinfo(
                "Settings Saved",
                "Settings have been saved successfully!\n\n"
                "The application will use these settings."
            )
            
            self.result = True
            self.window.destroy()

    def _on_cancel(self):
        """Handle cancel button click."""
        if self.is_first_run and not self.config.lcsc_api_key:
            response = messagebox.askyesno(
                "Exit Application",
                "API credentials are required to use this application.\n\n"
                "Do you want to exit?",
                icon=messagebox.WARNING
            )
            if response:
                self.result = False
                self.window.destroy()
        else:
            self.result = False
            self.window.destroy()

    def show(self) -> bool:
        """
        Show the dialog and wait for it to close.

        Returns:
            True if settings were saved, False if cancelled
        """
        self.window.wait_window()
        
        # Destroy window if standalone (shouldn't be needed but just in case)
        if self.standalone:
            try:
                self.window.destroy()
            except:
                pass
            
        return self.result if self.result is not None else False
