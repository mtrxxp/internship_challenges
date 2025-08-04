import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv()

DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()

if DB_TYPE == "postgres":
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "youtube_db")

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:

    sqlite_path = os.path.join(os.path.dirname(__file__), "databases", "influencers.db")
    DATABASE_URL = f"sqlite:///{sqlite_path}"

# SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False, future=True)


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)