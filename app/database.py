from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


SQL_ALCHEMY_DATABASE_URL = f"{settings.DATABASE_DRIVER}://{settings.DATABASE_USER}:{settings.DATABASE_PASSWOR}@{settings.DATABASE_HOSTNAME}/{settings.DATABASE_NAME}"

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(
#             host=HOST,
#             database=DATABASE_NAME,
#             user=USERNAME,
#             password=PASSWORD,
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Database connect")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error", error)
#         time.sleep(2)
