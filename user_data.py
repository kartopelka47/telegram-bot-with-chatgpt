import json
import sqlite3

DATA_FILE_PATH = "users_info.sqlite"

class User():
    def __init__(self, id, language, join_date):
        """
        :type language: str
        :type join_date: str or int
        :type id: str or int
        """
        self.id = id
        self.language = language
        self.join_date = str(join_date)

class DataBase():
    def __init__(self,data_path):
        self.data_path = data_path
        # self.user_id = user_id
        # self.data = self.getUser(
        #                     f"SELECT `user_id`, `language`, `join_date` FROM `user` WHERE `user_id` = '{}'")

    def IsNewbie(self, id):
        user = self.getUser(
            f"select `user_id` from `user` where `user_id` = '{id}'")
        if(user == None):
            return True
        return False

    def getUser(self, commandText):
        sqliteConnection = sqlite3.connect(self.data_path)
        DbCursor = sqliteConnection.cursor()
        returnedText = DbCursor.execute(commandText)
        returnedText = returnedText.fetchone()
        DbCursor.close()
        sqliteConnection.close()
        return returnedText

    def dbCommands(self, commandText):
        sqliteConnection = sqlite3.connect(self.data_path)
        DbCursor = sqliteConnection.cursor()
        DbCursor.execute(commandText)
        sqliteConnection.commit()
        DbCursor.close()
        sqliteConnection.close()

    # def __init__(self, data_path):
    #     self.data_path = data_path
    #
    #     with open(data_path, 'r+') as file:
    #         file_content = file.read()
    #         if len(file_content) == 0 or file_content.isspace():
    #             self.data = {}
    #             file.write(json.dumps(self.data))
    #         else:
    #             self.data = json.loads(file_content)
    #
    # def Update(self):
    #     with open(self.data_path, "w+") as file:
    #         json.dump(self.data, file)
    #
    # def IsNewbie(self, id):
    #     if str(id) in self.data:
    #         return False
    #
    #     return True
    #
    # def UpdateUser(self, user):
    #     self.data[user.id] = {"language": user.language,
    #                           "join_date":user.join_date}
    #     self.Update()
    #
    # def LoadUser(self, id):
    #     user_data = self.data[str(id)]
    #
    #     return User(id,
    #                 user_data["language"],
    #                 user_data["join_date"])