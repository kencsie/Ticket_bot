from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = 'ticket_bot'
    from .views import views

    app.register_blueprint(views, url_prefix='/')
    return app