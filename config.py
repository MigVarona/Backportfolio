import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI') or 'mongodb+srv://miguel:MIKy1969@cluster0.3hlzcty.mongodb.net/portfolio?retryWrites=true&w=majority'
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
