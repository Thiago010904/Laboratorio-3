import os
from app.core.config import settings
from sqlalchemy import create_engine, event, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


DATABASE_URL = settings.DATABASE_URL
DB_SCHEMA = settings.DB_SCHEMA

if not DATABASE_URL:
    raise ValueError(" No se encontró DATABASE_URL en el .env")

if not DB_SCHEMA:
    raise ValueError(" No se encontró DB_SCHEMA en el .env")


metadata = MetaData(schema=DB_SCHEMA)
Base = declarative_base(metadata=metadata)


engine = create_engine(
    DATABASE_URL,
    connect_args={"options": f"-c search_path={DB_SCHEMA}"}
)


@event.listens_for(engine, "connect")
def set_search_path(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute(f"SET search_path TO {DB_SCHEMA}")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()