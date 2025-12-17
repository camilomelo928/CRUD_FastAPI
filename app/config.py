from pydantic_settings import BaseSettings

class Settings(BaseSettings):
<<<<<<< HEAD
    DATABASE_URL: str = "mysql+pymysql://root:Popololo928.@127.0.0.1:3306/fastapi_demo?charset=utf8mb4"
    
=======
    DATABASE_URL: str = "mysql+pymysql://root:123456789@127.0.0.1:3306/fastapi_demo?charset=utf8mb4&auth_plugin=mysql_native_password"

>>>>>>> dcf3342b0e04c6a5160f14a56b0fbe51f9f37a2b
    class Config:
        env_file = ".env"

settings = Settings()

# Exportar las variables que database.py necesita
DATABASE_URL = settings.DATABASE_URL
IS_SQLITE = DATABASE_URL.startswith("sqlite")