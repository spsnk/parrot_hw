import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASS = os.getenv("POSTGRES_PASSWORD")
    DB_DB = os.getenv("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@db:5432/{DB_DB}" if DB_USER and DB_PASS and DB_DB else "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
