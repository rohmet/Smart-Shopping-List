from flask import Flask
from app.controllers.routes import route

app = Flask(__name__)

app.register_blueprint(route)