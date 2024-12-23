class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///event_management.db'  # Default DB (event_management)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SQLALCHEMY_BINDS = {
    #     'event_management': 'sqlite:///event_management.db',  # Event Management DB
    #     'accounts': 'sqlite:///accounts.db'  # Accounts DB
    # }

# class Config:
#     SECRET_KEY = 'your_secret_key'
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///event_management.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
