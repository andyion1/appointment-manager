import os

class Config:
    # Database configuration
    name = os.environ.get('DATABASE_NAME', 'db_proj_')
    user = os.environ.get('DATABASE_USER', '')
    password = os.environ.get('DATABASE_PASSWORD', '')
    host = os.environ.get('DATABASE_HOST', 'cspostgres.dawsoncollege.qc.ca')
    port = os.environ.get('DATABASE_PORT', '5432')
    
    # Flask configuration
    SECRET_KEY = 'dev_key_for_development_only'
    
    # Application settings
    DEBUG = True