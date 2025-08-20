import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application configuration settings."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL: str = os.getenv('OPENAI_MODEL', 'gpt-4')
    OPENAI_MAX_TOKENS: int = int(os.getenv('OPENAI_MAX_TOKENS', '2000'))
    OPENAI_TEMPERATURE: float = float(os.getenv('OPENAI_TEMPERATURE', '0.1'))
    
    # Application Configuration
    APP_NAME: str = "Insurance Claim Coverage Analyzer"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # File Processing Configuration
    MAX_FILE_SIZE: int = int(os.getenv('MAX_FILE_SIZE', '52428800'))  # 50MB
    SUPPORTED_FORMATS: list = ['pdf']
    TEMP_DIR: str = os.getenv('TEMP_DIR', '/tmp')
    
    # Analysis Configuration
    RED_FLAG_THRESHOLD: int = int(os.getenv('RED_FLAG_THRESHOLD', '3'))
    CONFIDENCE_THRESHOLD: float = float(os.getenv('CONFIDENCE_THRESHOLD', '0.7'))
    MAX_ANALYSIS_TIME: int = int(os.getenv('MAX_ANALYSIS_TIME', '300'))  # 5 minutes
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'app.log')
    
    # UI Configuration
    PAGE_TITLE: str = "Insurance Claim Analyzer"
    PAGE_ICON: str = "🚗"
    LAYOUT: str = "wide"
    
    @classmethod
    def get_openai_config(cls) -> Dict[str, Any]:
        """Get OpenAI configuration as dictionary."""
        return {
            'api_key': cls.OPENAI_API_KEY,
            'model': cls.OPENAI_MODEL,
            'max_tokens': cls.OPENAI_MAX_TOKENS,
            'temperature': cls.OPENAI_TEMPERATURE
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that all required configuration is present."""
        if not cls.OPENAI_API_KEY:
            return False
        return True

# Global settings instance
settings = Settings()
