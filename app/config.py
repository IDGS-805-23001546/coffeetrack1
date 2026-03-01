import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración base de la aplicación."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-dev'
    
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"mysql+pymysql://{os.environ.get('DB_USER', 'coffee_admin')}:" \
        f"{os.environ.get('DB_PASSWORD', 'Password_Coffee_2026')}@" \
        f"{os.environ.get('DB_HOST', 'localhost')}:" \
        f"{os.environ.get('DB_PORT', '3306')}/" \
        f"{os.environ.get('DB_NAME', 'coffeetrack')}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # True para debug SQL
    
    # Configuración de subida de archivos
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/img/uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}