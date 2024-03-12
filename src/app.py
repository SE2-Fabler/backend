from flask import Flask
from models import db
from views import views
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(views)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)