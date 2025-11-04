import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "tu_password_aqui")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
DATABASE_NAME = os.getenv("DATABASE_NAME", "blacklist_db")

#  NUEVO BLOQUE PARA DETECTAR DOCKER
if os.getenv("RUNNING_IN_DOCKER", "false").lower() == "true":
    DATABASE_HOST = "host.docker.internal"

DATABASE_URL = (
    f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

BEARER_TOKEN = os.getenv("BEARER_TOKEN", "my_static_token_123")
