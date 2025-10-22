"""
Configuration Management.

Handles application configuration from environment variables and config files.
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


class Config:
    """Application configuration."""
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            env_file: Path to .env file (optional)
        """
        # Load environment variables
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
        
        # Application metadata
        self.app_name = "LHAtoLCSC"
        self.version = "0.2.0"
        
        # API Configuration
        self.lcsc_api_key = os.getenv("LCSC_API_KEY", "")
        self.lcsc_api_secret = os.getenv("LCSC_API_SECRET", "")
        self.lcsc_api_url = os.getenv("LCSC_API_URL", "https://api.lcsc.com/v1")
        self.lcsc_api_base_url = os.getenv("LCSC_API_BASE_URL", "https://www.lcsc.com")
        self.request_timeout = int(os.getenv("REQUEST_TIMEOUT", "30"))
        self.lcsc_api_timeout = int(os.getenv("LCSC_API_TIMEOUT", "30"))
        self.lcsc_api_max_retries = int(os.getenv("LCSC_API_MAX_RETRIES", "3"))
        
        # Network Settings
        self.user_ip = os.getenv("USER_IP", "")
        
        # Application Settings
        self.default_currency = os.getenv("DEFAULT_CURRENCY", "USD")
        self.default_page_size = int(os.getenv("DEFAULT_PAGE_SIZE", "100"))
        self.fuzzy_match_threshold = int(os.getenv("FUZZY_MATCH_THRESHOLD", "75"))
        self.default_match_threshold = float(os.getenv("DEFAULT_MATCH_THRESHOLD", "0.70"))
        self.enable_cache = os.getenv("ENABLE_CACHE", "true").lower() == "true"
        self.cache_ttl_days = int(os.getenv("CACHE_TTL_DAYS", "7"))
        
        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE", "lhatolcsc.log")
        self.log_max_size = int(os.getenv("LOG_MAX_SIZE", "10485760"))  # 10MB
        self.log_backup_count = int(os.getenv("LOG_BACKUP_COUNT", "5"))
        
        # GUI Settings
        self.window_width = int(os.getenv("WINDOW_WIDTH", "1280"))
        self.window_height = int(os.getenv("WINDOW_HEIGHT", "800"))
        self.theme = os.getenv("THEME", "default")
        
        # Performance
        self.max_concurrent_requests = int(os.getenv("MAX_CONCURRENT_REQUESTS", "5"))
        self.request_delay_ms = int(os.getenv("REQUEST_DELAY_MS", "200"))
        self.batch_size = int(os.getenv("BATCH_SIZE", "50"))
        
        # Development
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.enable_profiling = os.getenv("ENABLE_PROFILING", "false").lower() == "true"
        
        # Paths
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.resources_dir = self.project_root / "resources"
        self.cache_dir = self.project_root / "cache"
        self.exports_dir = self.project_root / "exports"
        
        # Ensure directories exist
        self._create_directories()
    
    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        for directory in [self.cache_dir, self.exports_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def is_configured(self) -> bool:
        """
        Check if API credentials are configured.
        
        Returns:
            True if credentials are present, False otherwise
        """
        return bool(self.lcsc_api_key and self.lcsc_api_secret)
    
    def reload(self) -> None:
        """Reload configuration from environment variables."""
        load_dotenv(override=True)
        self.__init__()
    
    def get_cache_path(self, cache_name: str) -> Path:
        """
        Get path for a cache file.
        
        Args:
            cache_name: Name of the cache
            
        Returns:
            Path to cache file
        """
        return self.cache_dir / f"{cache_name}.cache"
    
    def get_export_path(self, filename: str) -> Path:
        """
        Get path for an export file.
        
        Args:
            filename: Name of the export file
            
        Returns:
            Path to export file
        """
        return self.exports_dir / filename
    
    def __repr__(self) -> str:
        """String representation (safe, no secrets)."""
        return (
            f"Config(app_name='{self.app_name}', "
            f"version='{self.version}', "
            f"api_configured={self.is_configured()}, "
            f"debug={self.debug})"
        )
