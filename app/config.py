import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Default to local MySQL database (adjust in your .env)
DATABASE_URL: str = "mysql+pymysql://root:Popololo928.@127.0.0.1:3306/fastapi_demo?charset=utf8mb4"
IS_SQLITE: bool = False