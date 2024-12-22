from app import create_app
from app.models import db

# Create app instance
app = create_app()

try:
    # Push the app context
    with app.app_context():
        # Create all tables
        db.create_all()

    print("Successfully Created DB")

except Exception as e:
    print(f"Setup Error:\n{e}")
