import os
from dotenv import load_dotenv

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
load_dotenv()

if os.environ['FLASK_ENV'] == 'test':
    DATABASE_URL = os.getenv('DATABASE_URL_TEST')
else:
    DATABASE_URL = os.getenv('DATABASE_URL')

# Database url
SQLALCHEMY_DATABASE_URI = DATABASE_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False
