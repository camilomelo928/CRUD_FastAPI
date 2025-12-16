from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://usuario:[CONFIGURE_ENV]@localhost:3306/fastapi_demo?charset=utf8mb4"
    
    class Config:
        env_file = ".env"

settings = Settings()
