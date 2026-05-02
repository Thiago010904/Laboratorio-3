from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData

# Definimos el schema globalmente en la metadata.
# Así, todos los modelos que hereden de 'Base' se crearán automáticamente 
metadata = MetaData(schema="jwt_grupo_7")

Base = declarative_base(metadata=metadata)