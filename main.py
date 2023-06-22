import openai
import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State
import logging
import aiogram.utils.markdown as md
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
import localization
import chatGPT
import user_data
import menu
import asyncio


TELEGRAM_API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")#Telegram_API_Token
OPENAI_API_TOKEN = os.environ.get("OPENAI_API_TOKEN")#openAI_API_Token
database = user_data.DataBase(user_data.DATA_FILE_PATH)


storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

class States(StatesGroup):
    search_info = State()


bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher(bot,storage=storage)


@dp.message_handler(types.ChatType.is_private, commands="search")
async def search_command(message: types.Message):
    user = user_data.User(message.from_user.id, "en", str(message.date))

    # load data about current user
    if database.IsNewbie(user.id):
        database.dbCommands(f"""INSERT INTO `user`(`user_id`,`language`,`join_date`)
        VALUES ('{user.id}','{user.language}','{user.join_date}')""")
    else:
        received_user_info = database.getUser(
            f"select `user_id`, `language`,`join_date` from `user` where `user_id` = '{user.id}'")
        user_id = received_user_info[0]
        user_language = received_user_info[1]
        user_join_date = received_user_info[2]
        user = user_data.User(user_id, user_language, user_join_date)

    States.search_info.set()
    bot.send_message(user.id, localization.write_search_query[user.language])


@dp.message_handler(state=States.search_info)
async def search_query(message: types.Message, state: FSMContext):
    user = user_data.User(message.from_user.id, "en", str(message.date))

    # load data about current user
    if database.IsNewbie(user.id):
        database.dbCommands(f"""INSERT INTO `user`(`user_id`,`language`,`join_date`) 
                VALUES ('{user.id}','{user.language}','{user.join_date}')""")
    else:
        received_user_info = database.getUser(
            f"select `user_id`, `language`,`join_date` from `user` where `user_id` = '{user.id}'")
        user_id = received_user_info[0]
        user_language = received_user_info[1]
        user_join_date = received_user_info[2]
        user = user_data.User(user_id, user_language, user_join_date)

    if message.text == "/search":
        search_command(message)
        state.finish()
        return
    elif message.text == "/start":
        start_command(message)
        state.finish()
        return

    bot.send_message(user.id, localization.processing_request[user.language])
    chatGPT_text = chatGPT.write_request(OPENAI_API_TOKEN, message.text)
    bot.send_message(user.id, chatGPT_text)
    state.finish()

@dp.message_handler(types.ChatType.is_private, commands="start")
async def start_command(message: types.Message):
    user = user_data.User(message.from_user.id, "en", str(message.date))

    # load data about current user
    if database.IsNewbie(user.id):
        database.dbCommands(f"""INSERT INTO `user`(`user_id`,`language`,`join_date`) 
                VALUES ('{user.id}','{user.language}','{user.join_date}')""")
    else:
        received_user_info = database.getUser(f"select `user_id`, `language`,`join_date` from `user` where `user_id` = '{user.id}'")
        user_id = received_user_info[0]
        user_language = received_user_info[1]
        user_join_date = received_user_info[2]
        user = user_data.User(user_id, user_language, user_join_date)

    bot.send_message(user.id, localization.choose_language[user.language], reply_markup=menu.get_language_menu())

@dp.callback_query_handler()
async def callback_handler(callback_query: types.CallbackQuery):
    user = user_data.User(callback_query.from_user.id, "en", str(callback_query.message.date))
    # load data about current user
    if database.IsNewbie(user.id):
        database.dbCommands(f"""INSERT INTO `user`(`user_id`,`language`,`join_date`) 
                VALUES ('{user.id}','{user.language}','{user.join_date}')""")
    else:
        received_user_info = database.getUser(
            f"select `user_id`, `language`,`join_date` from `user` where `user_id` = '{user.id}'")
        user_id = received_user_info[0]
        user_language = received_user_info[1]
        user_join_date = received_user_info[2]
        user = user_data.User(user_id, user_language, user_join_date)

    if callback_query.data == "uk" or "en":
        # user = database.LoadUser(callback_query.from_user.id)
        user.language = callback_query.data
        database.dbCommands(f"update `user` set `language`='{user.language}' where `user_id`='{user.id}'")

        bot.send_message(user.id, localization.choosed_language[user.language])
        return

if __name__ == '__main__':
    asyncio.run(executor.start_polling(dp, skip_updates=True))
