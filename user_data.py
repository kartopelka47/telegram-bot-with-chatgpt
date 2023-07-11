import sqlite3
import config


DATA_FILE_PATH = config.DATA_FILE_PATH
CREATE_TABLE_REQUEST = config.CREATE_TABLE_REQUEST


class User:
    def __init__(self, user_id, language, join_date, gpt_type):
        """
        :type user_id: str | int
        :type gpt_type: str
        :type language: str
        :type join_date: str | int
        """
        self.id = str(user_id)
        self.language = language
        self.join_date = str(join_date)
        self.GPT_type = gpt_type


class DataBase:
    def __init__(self, data_path):
        self.data_path = data_path

    def IsNewbie(self, id):
        user = self.get_info_from_database(
            f"select `user_id` from `user` where `user_id` = '{id}'")
        if not user:
            return True
        return False

    def get_info_from_database(self, commandText):
        sqliteConnection = sqlite3.connect(self.data_path)
        DbCursor = sqliteConnection.cursor()
        try:
            returnedText = DbCursor.execute(commandText)
        except sqlite3.OperationalError:
            DbCursor.execute(CREATE_TABLE_REQUEST)
            returnedText = DbCursor.execute(commandText)
        returnedText = returnedText.fetchall()
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
    if database.IsNewbie(user.id):
        database.dbCommands(f"""INSERT INTO `user`(`user_id`,`language`,`join_date`,`gpt_type`)
                        VALUES ('{user.id}','{user.language}','{user.join_date}','{user.GPT_type}')""")
    else:
        received_user_info = database.get_info_from_database(
            f"select `language`,`join_date`,`gpt_type` from `user` where `user_id` = '{user.id}'")
        user_language = received_user_info[0][0]
        user_join_date = received_user_info[0][1]
        user_gpt_type = received_user_info[0][2]
        user = User(user_id, user_language, user_join_date, user_gpt_type)
    return user
