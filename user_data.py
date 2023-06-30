import os
import sqlite3
import pyargon2

DATA_FILE_PATH = "users_info.sqlite"
HASH_SALT = os.environ.get("SALT")
CREATE_TABLE_REQUEST = """CREATE TABLE "user" (
	"id"	INTEGER NOT NULL UNIQUE,
	"user_id"	TEXT NOT NULL UNIQUE,
	"language"	INTEGER NOT NULL DEFAULT 'en',
	"join_date"	TEXT NOT NULL,
	"gpt_type"	TEXT NOT NULL DEFAULT 'default_gpt',
	PRIMARY KEY("id" AUTOINCREMENT)
)"""

class User:
    def __init__(self, user_id, language, join_date, gpt_type):
        """
        :type user_id: str | int
        :type gpt_type: str
        :type language: str
        :type join_date: str | int
        """
        self.id = user_id
        self.language = language
        self.join_date = str(join_date)
        self.hash_id = hash_text(str(user_id), str(HASH_SALT))
        self.GPT_type = gpt_type


class DataBase:
    def __init__(self, data_path):
        self.data_path = data_path

    def IsNewbie(self, id):
        user = self.getUser(
            f"select `user_id` from `user` where `user_id` = '{id}'")
        if not user:
            return True
        return False

    def getUser(self, commandText):
        sqliteConnection = sqlite3.connect(self.data_path)
        DbCursor = sqliteConnection.cursor()
        try:
            returnedText = DbCursor.execute(commandText)
        except sqlite3.OperationalError:
            DbCursor.execute(CREATE_TABLE_REQUEST)
            returnedText = DbCursor.execute(commandText)
        returnedText = returnedText.fetchone()
        DbCursor.close()
        sqliteConnection.close()
        return returnedText

    def dbCommands(self, commandText):
        sqliteConnection = sqlite3.connect(self.data_path)
        DbCursor = sqliteConnection.cursor()
        try:
            DbCursor.execute(commandText)
        except sqlite3.OperationalError:
            DbCursor.execute(CREATE_TABLE_REQUEST)
            DbCursor.execute(commandText)
        sqliteConnection.commit()
        DbCursor.close()
        sqliteConnection.close()


def user_login(database, user_id, login_date, gpt_type="default_gpt") -> User:
    """
    :type database: DataBase
    :type user_id: str or int
    :type login_date: str
    :type gpt_type: str
    """
    user = User(user_id, "en", str(login_date), gpt_type)

    # load data about current user
    if database.IsNewbie(user.hash_id):
        database.dbCommands(f"""INSERT INTO `user`(`user_id`,`language`,`join_date`,`gpt_type`)
                        VALUES ('{user.hash_id}','{user.language}','{user.join_date}','{user.GPT_type}')""")
    else:
        received_user_info = database.getUser(
            f"select `language`,`join_date`,`gpt_type` from `user` where `user_id` = '{user.hash_id}'")
        user_language = received_user_info[0]
        user_join_date = received_user_info[1]
        user_gpt_type = received_user_info[2]
        user = User(user_id, user_language, user_join_date, user_gpt_type)
    return user


def hash_text(text, salt) -> str:
    """
    :type text: str
    :type salt: str
    """
    _hash_text = pyargon2.hash(str(text), str(salt), hash_len=32, time_cost=1,
                               memory_cost=16, variant="id", parallelism=2)
    return _hash_text
