from sqlalchemy.orm.session import Session


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from core.settings import DATABASE_URL


# create db connection
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker[Session](autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


