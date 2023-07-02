import os
TELEGRAM_API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")
OPENAI_API_TOKEN = os.environ.get("OPENAI_API_TOKEN")
ADMIN_USER = os.environ.get("ADMIN_USER")
HASH_SALT = os.environ.get("SALT")
BOT_NAME = os.environ.get("BOT_NAME")
DATA_FILE_PATH = "users_info.sqlite"
CREATE_TABLE_REQUEST = """CREATE TABLE "user" (
	"id"	INTEGER NOT NULL UNIQUE,
	"user_id"	TEXT NOT NULL UNIQUE,
	"language"	INTEGER NOT NULL DEFAULT 'en',
	"join_date"	TEXT NOT NULL,
	"gpt_type"	TEXT NOT NULL DEFAULT 'default_gpt',
	PRIMARY KEY("id" AUTOINCREMENT)
)"""