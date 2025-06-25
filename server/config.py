# server/config.py

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///plants.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False