# app/main.py
from flask import Blueprint, render_template, redirect, url_for, request, flash, send_file
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models import User
from app.forms import LoginForm, UploadForm
from app.utils import add_text_behind_image
import os

bp = Blueprint('main', __name__)

@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = UploadForm()
    if form.validate_on_submit():
        image = form.image.data
        text = form.text.data
        processed_path = add_text_behind_image(image, text)

        # Get the absolute path to the static/uploads directory
        processed_filename = os.path.basename(processed_path)
        static_path = os.path.join(os.getcwd(), 'app', 'static', 'uploads', processed_filename)

        # Serve the image from the correct static/uploads directory
        return send_file(static_path, as_attachment=True, download_name=processed_filename)

    return render_template("index.html", form=form)

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('main.index'))  # Corrected url_for to use 'main.index'
        flash("Login Unsuccessful. Check username and password.", "danger")
    return render_template("login.html", form=form)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))  # Corrected url_for to use 'main.login'

# from flask import Blueprint, render_template, redirect, url_for, request, flash, send_file, current_app
# from flask_login import login_user, logout_user, login_required, current_user
# from app import db, login_manager  # Import app and db from app
# from app.models import User
# from app.forms import LoginForm, UploadForm
# from app.utils import add_text_behind_image
# import os

# bp = Blueprint('main', __name__)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# @bp.route("/", methods=["GET", "POST"])
# @login_required
# def index():
#     form = UploadForm()
#     if form.validate_on_submit():
#         image = form.image.data
#         text = form.text.data
#         processed_path = add_text_behind_image(image, text)

#         # Get the absolute path to the static/uploads directory
#         processed_filename = os.path.basename(processed_path)
#         static_path = os.path.join(os.getcwd(), 'app', 'static', 'uploads', processed_filename)

#         # Serve the image from the correct static/uploads directory
#         return send_file(static_path, as_attachment=True, download_name=processed_filename)

#     return render_template("index.html", form=form)

# @bp.route("/login", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user and user.password == form.password.data:
#             login_user(user)
#             return redirect(url_for('main.index'))  # Corrected url_for to use 'main.index'
#         flash("Login Unsuccessful. Check username and password.", "danger")
#     return render_template("login.html", form=form)

# @bp.route("/login/google")
# def login_google():
#     # Redirect to Google OAuth 2.0 login
#     redirect_uri = url_for('main.auth', _external=True)
#     google = current_app.google  # Access the google OAuth client from the app context
#     return google.authorize_redirect(redirect_uri)

# @bp.route("/auth")
# def auth():
#     # Handle Google OAuth callback
#     google = current_app.google  # Access the google OAuth client from the app context
#     token = google.authorize_access_token()
#     user_info = google.parse_id_token(token)

#     # Check if user already exists in the database, otherwise create a new user
#     user = User.query.filter_by(email=user_info['email']).first()
#     if user is None:
#         user = User(username=user_info['name'], email=user_info['email'])
#         db.session.add(user)
#         db.session.commit()

#     login_user(user)
#     return redirect(url_for('main.index'))  # Redirect to the main page after login

# @bp.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('main.login'))  # Corrected url_for to use 'main.login'


