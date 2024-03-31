from flask import Flask
from . import db
from . import auth
from . import story
from src.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(story.bp)

    return app