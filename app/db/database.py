import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# Obtener la URL de conexión a PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Configurar la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia de FastAPI para manejar la sesión de base de datos
def get_db():
    """
    Crea una nueva sesión de base de datos para cada petición (request)
    y se asegura de cerrarla cuando la petición termina.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()