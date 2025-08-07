"""
Configuration management for Portfolio Manager
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration settings"""
    
    # Database settings
    DATABASE_PATH = os.getenv('DATABASE_PATH', './data/portfolio.db')
    
    # Date format settings
    DATE_FORMAT = '%d/%m/%Y'
    DATE_FORMAT_DISPLAY = 'dd/mm/yyyy'
    
    # Currency settings
    DEFAULT_CURRENCY = 'GBP'
    
    # yfinance settings
    YFINANCE_TIMEOUT = 30
    PRICE_UPDATE_BATCH_SIZE = 10
    
    # Streamlit settings
    PAGE_TITLE = "Portfolio Manager"
    PAGE_ICON = "📈"
    LAYOUT = "wide"
    
    @classmethod
    def ensure_data_directory(cls):
        """Ensure the data directory exists"""
        data_dir = Path(cls.DATABASE_PATH).parent
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir
    
    @classmethod
    def get_database_url(cls):
        """Get the SQLAlchemy database URL"""
        cls.ensure_data_directory()
        return f"sqlite:///{cls.DATABASE_PATH}"