from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():

    load_dotenv()

    app = Flask(__name__)   
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    from .routes import main
    app.register_blueprint(main)


    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app