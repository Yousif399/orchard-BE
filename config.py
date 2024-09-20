from flask import Flask
import flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask_jwt_extended import JWTManager
load_dotenv()


app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "SQLALCHEMY_DATABASE_URI")


app.config["CLOUDINARY_CLOUD_NAME"] = os.environ.get('CLOUDINARY_CLOUD_NAME')
app.config["CLOUDINARY_API_KEY"] = os.environ.get('CLOUDINARY_API_KEY')
app.config["CLOUDINARY_API_SECRET"] = os.environ.get('CLOUDINARY_API_SECRET')

app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')


cloudinary.config(
    cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
    api_key=app.config['CLOUDINARY_API_KEY'],
    api_secret=app.config['CLOUDINARY_API_SECRET']
)
db = SQLAlchemy(app)
jwt = JWTManager(app)

