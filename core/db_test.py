from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import get_settings

settings = get_settings()

DATABASE_URL_TEST = settings.DATABASE_URL_TEST

enginetest = create_engine(
    DATABASE_URL_TEST,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL_TEST else {},
)
SessionLocalTest = sessionmaker(autocommit=False, autoflush=False, bind=enginetest)
Basetest = declarative_base()
