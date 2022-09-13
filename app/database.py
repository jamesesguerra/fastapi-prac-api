from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = settings.db_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# db connection only for psycopg2
# import psycopg2
# from psycopg2.extras import RealDictCursor
# from time import sleep
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='james', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successful!')
#         break
#     except Exception as error:
#         print('Connecting to DB failed...')
#         print(f"Error: {error}")
#         sleep(2)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()