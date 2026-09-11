import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SUPABASE_URL = os.getenv("SUPABASE_URL")

engine = create_engine(SUPABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
