from flask import Flask
from app.routes import main
from settings import config
import os

def create_app(config_class=config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    

    app.register_blueprint(main)
    return app

