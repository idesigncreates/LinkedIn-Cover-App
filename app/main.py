# app/main.py
from flask import Blueprint, render_template, redirect, url_for, request, flash, send_file
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models import User
from app.forms import LoginForm, UploadForm
from app.utils import add_text_behind_image
import os
from werkzeug.utils import secure_filename


bp = Blueprint('main', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = UploadForm()
    uploaded_image_url = None
    processed_image_url = None
    processed_image_path = None  # Keep track of the processed image path for download

    if form.validate_on_submit():
        image = form.image.data
        text = form.text.data

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            # Save the uploaded image
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)

            # Add text to the uploaded image
            processed_path = add_text_behind_image(image_path, text)

            # Generate URLs for the uploaded and processed images
            uploaded_image_url = url_for('static', filename='uploads/' + filename)
            processed_filename = os.path.basename(processed_path)
            processed_image_url = url_for('static', filename='uploads/' + processed_filename)
            processed_image_path = processed_filename  # Store the correct filename for download link

            return render_template("index.html", form=form, uploaded_image_url=uploaded_image_url, processed_image_url=processed_image_url, processed_image_path=processed_image_path)

        else:
            flash("Invalid file type. Only image files are allowed.", "danger")

    return render_template("index.html", form=form, uploaded_image_url=uploaded_image_url, processed_image_url=processed_image_url, processed_image_path=processed_image_path)



@bp.route("/download/<filename>")
def download_file(filename):
    # Send the processed image file as an attachment for download
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

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



