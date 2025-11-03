import os
from dotenv import load_dotenv

# Cargar variables del archivo .env si existe
load_dotenv()

# Datos de conexión a PostgreSQL (puedes definirlos en tu archivo .env)
DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "tu_password_aqui")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
DATABASE_NAME = os.getenv("DATABASE_NAME", "blacklist_db")

# URL de conexión SQLAlchemy
# Para pruebas con SQLite (comentar para usar PostgreSQL)
#DATABASE_URL = "sqlite:///emails.db"

# Para PostgreSQL (descomentar cuando tengas PostgreSQL configurado)
DATABASE_URL = (
    f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

# Token estático para autenticación
BEARER_TOKEN = os.getenv("BEARER_TOKEN", "my_static_token_123")
