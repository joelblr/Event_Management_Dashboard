from server import create_server
from server.models import db

# Create server instance
server = create_server()

try:
    # Push the server context
    with server.server_context():
        # Create all tables
        db.create_all()

    print("Successfully Created DB")

except Exception as e:
    print(f"Setup Error:\n{e}")
