from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://root:123456789@127.0.0.1:3306/fastapi_demo?charset=utf8mb4&auth_plugin=mysql_native_password"

    class Config:
        env_file = ".env"

settings = Settings()

# Exportar las variables que database.py necesita
DATABASE_URL = settings.DATABASE_URL
IS_SQLITE = DATABASE_URL.startswith("sqlite")