import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

def get_env_var(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise EnvironmentError(f"La variable de entorno obligatoria '{name}' no está definida en el archivo .env")
    return value

# Configuración de base de datos
DATABASE_URL = get_env_var("DATABASE_URL")

# Configuración de JWT
SECRET_KEY = get_env_var("SECRET_KEY")
ALGORITHM = get_env_var("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(get_env_var("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Otros parámetros
DEBUG = get_env_var("DEBUG").lower() == "true"
ENV = get_env_var("ENV")

# Seguridad IP (si son obligatorias, también se validan)
MAX_SESSIONS_PER_IP = int(get_env_var("MAX_SESSIONS_PER_IP"))
MAX_CONNECTIONS_PER_IP = int(get_env_var("MAX_CONNECTIONS_PER_IP"))
BLOCK_DURATION_MINUTES = int(get_env_var("BLOCK_DURATION_MINUTES"))
