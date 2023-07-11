import user_data
from config import BOT_NAME


database = user_data.DataBase(user_data.DATA_FILE_PATH)


async def user_profile(user) -> str:
    """
    :type user: user_data.User
    """
    user_profile_dict = {
        "uk":f"""
Id: <code>{user.id}</code>
Мова: {user.language}
Дата приєднання: {user.join_date}
GPT тип: {user.GPT_type}
        """,
        "en":f"""
Id: <code>{user.id}</code>
Language: {user.language}
Date of joining: {user.join_date}
GPT type: {user.GPT_type}"""
    }
    return user_profile_dict[user.language]


async def bot_info(language) -> str:
    """
    :type language: user_data.User.language
    """
    _info = database.get_info_from_database("SELECT count(user_id),SUM(`requests`) FROM user")
    user_count = _info[0][0]
    requests_count = _info[0][1]
    bot_info_dict = {
        "uk": f"""
Кількість користувачів: {user_count}
Кількість запитів: {requests_count}
            """,
        "en": f"""
Count of users: {user_count}
Count of requests: {requests_count}"""
    }
    return bot_info_dict[language]


choose_language = {
    "uk":"Оберіть мову",
    "en":"Choose language"
}

service_unavailable_error = {
    "uk":"Сервер перегружений, або тимчасово не доступний. Будь ласка спробуйте пізніше",
    "en":"The server is overloaded or temporarily unavailable. Please try again later"
}

ukrainisation = {
    "uk":"Українізація",
    "en":"Ukrainisation"
}

select_gpt_type = {
    "uk":"Оберіть тип gpt",
    "en":"Select a gpt type"
}

default = {
    "uk":"Стандартний",
    "en":"Default"
}

user = {
    "uk":"Користувач",
    "en":"User"
}

try_again_later = {
    "uk":"Повторіть запит пізніше",
    "en":"Try again later"
}

info = {
    "uk":f"""
Мене звати {BOT_NAME}
Я бот працюючий за допомоги ChatGPT
Cписок команд:
/commands
""",
    "en":f"""
My name is {BOT_NAME}
I am a bot working with the help of ChatGPT
List of commands:    
/commands"""
}

commands_list = {
    "uk":"""
/start - початок роботи з ботом
/info - інформація про бота
/commands - список команд
/language - мова
/feedback - зворотній зв'язок
/search - пошук
/type - вибрати тип GPT, який ви бажаєте
/profile - ваш профіль
/payment - фінансова допомога
/cancel - відмінити поточну дію
    """,
    "en":"""
/start - start working with the bot
/info - information about the bot
/commands - list of commands
/language - change language
/feedback - feedback
/search - search 
/type - select the type of GPT you want
/profile - your profile
/payment - financial support
/cancel - cancel currently operation
"""
}


admin_command_list = {
    "uk":"""
/start - початок роботи з ботом
/info - інформація про бота
/commands - список команд
/language - мова
/feedback - зворотній зв'язок
/search - пошук
/type - вибрати тип GPT, який ви бажаєте
/profile - ваш профіль
/payment - фінансова допомога
/stats - статистика бота
/message - розсилка повідомлень
/cancel - відмінити поточну дію
    """,
    "en":"""
/start - start working with the bot
/info - information about the bot
/commands - list of commands
/language - change language
/feedback - feedback
/search - search 
/type - select the type of GPT you want
/profile - your profile
/payment - financial support
/stats - bot statistic
/message - message distribution
/cancel - cancel currently operation
"""
}


greetings = {
    "uk":"Вітаю, більше інформації по команді: /info",
    "en":"Greetings, more information: /info"
}

report = {
    "uk":"Прийшов репорт",
    "en":"The report came"
}

thanks_for_report = {
    "uk":"Дякуємо за ваш фідбек",
    "en":"Thanks for your report"
}

feedback = {
    "uk":"Опишіть свою проблему",
    "en":"Describe your problem"
}

choosed_language ={
    "uk":"Ви обрали 🇺🇦Українська",
    "en":"You have chosen 🇬🇧English"
}

write_search_query = {
    "uk":"Введіть пошуковий запит",
    "en":"Enter search query"
}

processing_request = {
    "uk":"Очікуйте, обробляємо запит...",
    "en":"Wait, processing the request..."
}

choosed_types = {
    "uk":{
        "ukrainisation_gpt":"Ви обрали українізовану версію",
        "default_gpt":"Ви обрали стандартну версію"
    },
    "en":{
        "ukrainisation_gpt":"You have selected the Ukrainianised version",
        "default_gpt":"You have selected the standard version"
    }
}

message_with_cancel = {
    "uk":"Якщо ви хочете відмінити дію, напишіть /cancel",
    "en":"If you want to cancel the action, write /cancel"
}

action_canceled = {
    "uk":"Дію відхилену",
    "en":"Action canceled"
}

payment_help = {
    "uk":"Якщо ви бажаєте допомогти в розробці бота, то станьте нашим патроном",
    "en":"If you want to help with the development of the bot, become our patron"
}

help_translate = {
    "uk":"Допомогти",
    "en":"Help"
}

send_message = {
    "uk":"Напишіть повідомлення, воно буде переслано всім користувачам бота",
    "en":"Write a message, it will be sent to all users of the bot"
}