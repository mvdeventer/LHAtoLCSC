"""
Main entry point for LHAtoLCSC application.
"""

import sys
import tkinter as tk
from tkinter import messagebox

from lhatolcsc.core.config import Config
from lhatolcsc.core.logger import setup_logger
from lhatolcsc.gui.main_window import MainWindow
from lhatolcsc.gui.settings_dialog import SettingsDialog


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
        
        # Check if this is first run (no credentials configured)
        if not config.is_configured():
            logger.info("First run detected - showing setup wizard")
            
            # For first run, create the wizard as the main window
            # Don't create a separate root window yet
            wizard = SettingsDialog(None, config, is_first_run=True)
            result = wizard.show()
            
            if not result:
                # User cancelled setup
                logger.info("User cancelled first-run setup - exiting")
                return 0
            
            # Reload config after setup
            config.reload()
            logger.info("Configuration updated from setup wizard")
        else:
            logger.info("API credentials already configured")
        
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
        try:
            messagebox.showerror(
                "Fatal Error",
                f"An unexpected error occurred:\n\n{str(e)}\n\n"
                "Please check the log file for details."
            )
        except:
            pass
        return 1


if __name__ == "__main__":
    sys.exit(main())
