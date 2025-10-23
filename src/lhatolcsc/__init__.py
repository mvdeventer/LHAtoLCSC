"""
LHAtoLCSC - BOM to LCSC Part Matcher

A professional desktop application for matching Bill of Materials components
with LCSC electronic parts using intelligent fuzzy search.
"""

__version__ = "0.2.4"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__license__ = "MIT"

from lhatolcsc.core.config import Config
from lhatolcsc.core.logger import setup_logger

__all__ = ["Config", "setup_logger"]
