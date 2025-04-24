import os

class Config:
<<<<<<< HEAD
    name = os.environ.get('DATABASE_NAME', 'dbproj')
=======
    # Database configuration
    name = os.environ.get('DATABASE_NAME', 'db_proj_')
>>>>>>> 919741f2335c17c05d95d1eb1567e82edb0cc552
    user = os.environ.get('DATABASE_USER', '')
    password = os.environ.get('DATABASE_PASSWORD', '')
    host = os.environ.get('DATABASE_HOST', 'cspostgres.dawsoncollege.qc.ca')
    port = os.environ.get('DATABASE_PORT', '5432')
<<<<<<< HEAD

    SECRET_KEY = 'dev_key_for_development_only'

=======
    
    # Flask configuration
    SECRET_KEY = 'dev_key_for_development_only'
    
    # Application settings
>>>>>>> 919741f2335c17c05d95d1eb1567e82edb0cc552
    DEBUG = True