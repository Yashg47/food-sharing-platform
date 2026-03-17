import os

class Config:
    SECRET_KEY = os.getenv("232", "supersecret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/fooddb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
