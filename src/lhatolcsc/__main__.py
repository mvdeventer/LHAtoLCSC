"""
Main entry point for LHAtoLCSC application.
"""

import sys
import tkinter as tk
from tkinter import messagebox

from lhatolcsc.core.config import Config
from lhatolcsc.core.logger import setup_logger
from lhatolcsc.gui.main_window import MainWindow


def main() -> int:
    """
    Main entry point for the application.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # Setup logging
    logger = setup_logger()
    logger.info("Starting LHAtoLCSC application")
    
    try:
        # Load configuration
        config = Config()
        logger.info(f"Configuration loaded: {config.app_name} v{config.version}")
        
        # Validate API credentials
        if not config.lcsc_api_key or not config.lcsc_api_secret:
            logger.warning("API credentials not configured")
            messagebox.showwarning(
                "Configuration Required",
                "LCSC API credentials are not configured.\n\n"
                "Please edit the .env file and add your API key and secret.\n"
                "You can obtain these from: https://www.lcsc.com/agent"
            )
        
        # Create main window
        root = tk.Tk()
        app = MainWindow(root, config)
        
        logger.info("Application GUI initialized")
        
        # Start main loop
        root.mainloop()
        
        logger.info("Application closed normally")
        return 0
        
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        messagebox.showerror(
            "Fatal Error",
            f"An unexpected error occurred:\n\n{str(e)}\n\n"
            "Please check the log file for details."
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
