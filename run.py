import logging
from app import create_app, db
from app.models import User  # Import all your models here

# Configure logging
logging.basicConfig(
    filename='logs/app.log',   # Log file specifically for setup
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def setup_database():
    app = create_app()

    # Initialize the app with an application context
    with app.app_context():
        try:
            logging.info("Starting database setup...")
            db.create_all()  # Create all tables defined in models
            logging.info("Database tables created successfully.")
        except Exception as e:
            logging.error("Error occurred during database setup: %s", str(e))

def run_app():
    app = create_app()
    app.run(debug=True)  # Start the Flask app

if __name__ == "__main__":
    # setup_database()
      run_app() 
