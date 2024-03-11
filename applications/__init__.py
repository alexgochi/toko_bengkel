from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager, UserMixin,\
    login_required, login_user, logout_user, AnonymousUserMixin
from flask import sessions

# db = SQLAlchemy()
login_manager = LoginManager()


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.absen = 'Guest'


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    CORS(app)
    # app.config.from_object('config.Config')
    # db.init_app(app)
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.anonymous_user = Anonymous

    with app.app_context():
        from applications.controller import LoginController, ErrorController, MemberController, RekeningController

    return app
