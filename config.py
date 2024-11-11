import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:8080/helix_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecret")
