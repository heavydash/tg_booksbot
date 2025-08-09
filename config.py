import os
from dotenv import load_dotenv
import os

load_dotenv()
print("Loading .env file:", os.getenv("API_TOKEN"))

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN not found in .env file")
DATABASE_URL = "sqlite+aiosqlite:///books.db"
BOOKS_DIR = "books"
ADMIN_IDS=[276798285]
