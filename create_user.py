# create_user.py
from app import create_app, db
from app.models import User

# Initialize the Flask app and create the database
app = create_app()

# Create tables if they don't exist
with app.app_context():
    db.create_all()

    # Check if a user already exists
    user = User.query.filter_by(username='admin').first()
    if not user:
        # Add a default user
        new_user = User(username='admin', password='password123')  # Use a simple password for now
        db.session.add(new_user)
        db.session.commit()

    print("User created or already exists.")
