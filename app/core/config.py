import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super_secret_key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
    )

    # Base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL")

  
    DB_SCHEMA: str = os.getenv("DB_SCHEMA")

    def validate(self):
        """
        Validaciones obligatorias al iniciar la app
        """
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL no está configurado en el .env")

        if not self.DB_SCHEMA:
            raise ValueError("DB_SCHEMA no está configurado en el .env")

        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY no está configurado")


# Instancia global
settings = Settings()

# Ejecutar validaciones al importar
settings.validate()