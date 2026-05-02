import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 1. Localizar el .env
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("🚨 No se encontró DATABASE_URL en el .env")

# 2. Configurar el motor con el esquema por defecto
# connect_args le dice a PostgreSQL que busque siempre en tu esquema
engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-c search_path=jwt_grupo_7"}
)

# 3. Forzar el esquema en cada conexión (Doble seguridad)
@event.listens_for(engine, "connect")
def set_search_path(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("SET search_path TO jwt_grupo_7")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()