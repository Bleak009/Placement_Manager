import os

DB_HOST = 'localhost'
DB_NAME = 'placement'
DB_USER = 'root'
DB_PASSWORD = '120404'
UPLOAD_FOLDER = "app/static/uploads/"

connection = None
mycursor = None

class config:
    SECRET_KEY = 'scythevyse'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
