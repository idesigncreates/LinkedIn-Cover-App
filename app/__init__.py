# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()  # Initialize SQLAlchemy instance
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)  # Initialize db with the app context
    login_manager.init_app(app)

    # Set login_view to the correct blueprint and route
    login_manager.login_view = 'main.login'  # Reference the 'login' route in the 'main' blueprint

    # Import models after db initialization
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# from authlib.integrations.flask_client import OAuth  # Import OAuth from authlib
# from config import Config

# db = SQLAlchemy()  # Initialize SQLAlchemy instance
# login_manager = LoginManager()

# # Initialize OAuth instance
# oauth = OAuth()

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     db.init_app(app)  # Initialize db with the app context
#     login_manager.init_app(app)

#     # Initialize OAuth with the app context
#     oauth.init_app(app)

#     # Register google oauth client here
#     google = oauth.register(
#         'google',
#         client_id='your-client-id',
#         client_secret='your-client-secret',
#         authorize_url='https://accounts.google.com/o/oauth2/auth',
#         authorize_params=None,
#         access_token_url='https://accounts.google.com/o/oauth2/token',
#         refresh_token_url=None,
#         api_base_url='https://www.googleapis.com/oauth2/v1/',
#         client_kwargs={'scope': 'openid profile email'},
#     )

#     # Attach google to the app
#     app.google = google  # Make google available in the app context

#     # Set login_view to the correct blueprint and route
#     login_manager.login_view = 'main.login'  # Reference the 'login' route in the 'main' blueprint

#     # Import models after db initialization
#     from app.models import User

#     @login_manager.user_loader
#     def load_user(user_id):
#         return User.query.get(int(user_id))

#     # Register blueprints
#     from app.main import bp as main_bp
#     app.register_blueprint(main_bp)

#     return app

