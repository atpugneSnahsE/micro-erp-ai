import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "360"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database/erp.db")
BACKUP_ENCRYPTION_KEY = os.getenv("BACKUP_ENCRYPTION_KEY")
