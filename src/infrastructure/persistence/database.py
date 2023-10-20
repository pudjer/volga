import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = os.environ.get('POSTGRES_USER')
db = os.environ.get('POSTGRES_DB')
password = os.environ.get('POSTGRES_PASSWORD')

SQLALCHEMY_DATABASE_URL = f'postgresql://{user}:{password}@postgres/{db}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
