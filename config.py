import os

TELEGRAM_API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")
OPENAI_API_TOKEN = os.environ.get("OPENAI_API_TOKEN")
ADMIN_USER = os.environ.get("ADMIN_USER")
PAYMENT_LINK = os.environ.get("PAYMENT_LINK")
BOT_NAME = os.environ.get("BOT_NAME")
TIME_FORMAT = "%H:%M %d.%m.%y"
DATA_FILE_PATH = "users_info.sqlite"
CREATE_TABLE_REQUEST = """CREATE TABLE "user" (
"id"	INTEGER NOT NULL UNIQUE,
"user_id"	TEXT NOT NULL UNIQUE,
"language"	INTEGER NOT NULL DEFAULT 'en',
"join_date"	TEXT NOT NULL,
"gpt_type"	TEXT NOT NULL DEFAULT 'default_gpt',
"requests"	INTEGER NOT NULL DEFAULT 0,PRIMARY KEY("id" AUTOINCREMENT)
);"""
