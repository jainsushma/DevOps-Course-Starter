import os

class Config:
    """Base configuration variables."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    LOGIN_DISABLED = os.getenv('LOGIN_DISABLED')=="True"
    LOG_LEVEL = os.getenv('LOG_LEVEL')
    LOGGLY_TOKEN = os.getenv('LOGGLY_TOKEN')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
