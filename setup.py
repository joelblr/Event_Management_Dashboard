from server import create_server
from server.models import db

# Create server instance
server = create_server()

try:
    # Push the server context
    with server.app_context():
        # Create all tables
        db.create_all()
    print("All databases and tables created successfully!")

    print("Successfully ensured tables for accounts DB")

except Exception as e:
    print(f"Setup Error:\n{e}")
