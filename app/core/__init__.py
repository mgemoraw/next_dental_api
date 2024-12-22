# from dotenv import load_dotenv
import os

from .config import BASE_DIR, get_settings, SECRET_KEY, ALGORITHM
from .database import SessionLocal

from .deps import get_db 

# load_dotenv()
