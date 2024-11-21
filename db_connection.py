from sqlalchemy import create_engine
from config import DATABASE_URI

engine = create_engine(DATABASE_URI)

def get_db_connection():
    return engine.connect()
