import os
import aiogram
import openai
from aiogram import Bot, Dispatcher, executor, types
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import localization
import chatGPT
import user_data
import menu
import config

BOT_NAME = config.BOT_NAME

TELEGRAM_API_TOKEN = config.TELEGRAM_API_TOKEN
OPENAI_API_TOKEN = config.OPENAI_API_TOKEN
ADMIN_USER = config.ADMIN_USER
HASH_SALT = config.HASH_SALT
database = user_data.DataBase(user_data.DATA_FILE_PATH)

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)


class States(StatesGroup):
    search_info = State()
    feedback_state = State()
    send_message_state = State()


bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher(bot, storage=storage)


async def check_message_for_func(message, state):
    if message.text == "/search":
        await state.finish()
        await search_command(message)
        return True
    elif message.text == "/start":
        await state.finish()
        await start_command(message)
        return True
    elif message.text == "/info":
        await state.finish()
        await info_about_bot(message)
        return True
    elif message.text == "/commands":
        await state.finish()
        await commands(message)
        return True
    elif message.text == "/feedback":
        await state.finish()
        await feedback(message)
        return True
    elif message.text == "/language":
        await state.finish()
        await choose_language(message)
        return True
    elif message.text == "/type":
        await state.finish()
        await change_type(message)
        return True


@dp.message_handler(types.ChatType.is_private, commands="info")
async def info_about_bot(message: types.Message):
    user = user_data.user_login(database, message.from_user.id, message.date.strftime("%H:%M %d.%m.%y"))
    await bot.send_message(user.id, localization.info[user.language])


@dp.message_handler(types.ChatType.is_private, commands="commands")
async def commands(message: types.Message):
    user = user_data.user_login(database, message.from_user.id, message.date.strftime("%H:%M %d.%m.%y"))
    await bot.send_message(user.id, localization.commands_list[user.language])


@dp.message_handler(types.ChatType.is_private, commands="feedback")
async def feedback(message: types.Message):
    user = user_data.user_login(database, message.from_user.id, message.date.strftime("%H:%M %d.%m.%y"))
    await States.feedback_state.set()
    await bot.send_message(user.id, localization.feedback[user.language])


@dp.message_handler(types.ChatType.is_private, commands="language")
async def choose_language(message: types.Message):
    user = user_data.user_login(database, message.from_user.id, message.date.strftime("%H:%M %d.%m.%y"))

    await bot.send_message(user.id, localization.choose_language[user.language],
                           reply_markup=menu.get_language_menu())


@dp.message_handler(types.ChatType.is_private, commands="search")
async def search_command(message: types.Message):
    user = user_data.user_login(database, message.from_user.id, message.date.strftime("%H:%M %d.%m.%y"))
    await States.search_info.set()
    await bot.send_message(user.id, localization.write_search_query[user.language])


@dp.message_handler(state=States.feedback_state)
async def get_feedback(message: types.Message, state: FSMContext):
    user = user_data.user_login(database, message.from_user.id, message.date.strftime("%H:%M %d.%m.%y"))
    admin_user = user_data.user_login(database, ADMIN_USER, message.date.strftime("%H:%M %d.%m.%y"))

    if await check_message_for_func(message, state):
        return

    await bot.send_message(admin_user.id, f"""
    {localization.report[admin_user.language]}
{message.date.strftime("%H:%M %d.%m.%y")}
{message.text}""", reply_markup=menu.user_from_tgUrl(admin_user.language, message.from_user.url))
    await bot.send_message(user.id, localization.thanks_for_report[user.language])


@dp.message_handler(state=States.search_info)
async def search_query(message: types.Message, state: FSMContext):
    user = user_data.user_login(database, message.from_user.id, message.date.strftime("%H:%M %d.%m.%y"))
    if await check_message_for_func(message, state):
        return

    await bot.send_message(user.id, localization.processing_request[user.language])

    chat = chatGPT.GPT(OPENAI_API_TOKEN, message.text)
    chat.request_text = message.text
    response = await chat.choose_gpt_type(user.GPT_type)
    # try:
    #     response = await chat.standart_request()
    # except openai.error.RateLimitError:
    #     response = localization.try_again_later[user.language]
    # except openai.error.ServiceUnavailableError:
    #     response = localization.service_unavailable_error[user.language]
    await bot.send_message(user.id, response)
    await state.finish()


@dp.message_handler(types.ChatType.is_private, commands="start")
async def start_command(message: types.Message):
    user = user_data.user_login(database, message.from_user.id, message.date.strftime("%H:%M %d.%m.%y"))
    if database.IsNewbie(user.hash_id):
        await bot.send_message(user.id, localization.choose_language[user.language],
                               reply_markup=menu.get_language_menu())
    await bot.send_message(user.id, localization.greetings[user.language])


@dp.message_handler(types.ChatType.is_private, commands="type")
async def change_type(message: types.Message):
    user = user_data.user_login(database, message.from_user.id, message.date.strftime("%H:%M %d.%m.%y"))
    await bot.send_message(user.id, localization.select_gpt_type[user.language],
                           reply_markup=menu.change_bot_type(user.language))


@dp.callback_query_handler()
async def callback_handler(callback_query: types.CallbackQuery):
    user = user_data.user_login(database, callback_query.from_user.id,
                                callback_query.message.date.strftime("%H:%M %d.%m.%y"))

    if callback_query.data == "uk" or callback_query.data == "en":
        user.language = callback_query.data
        database.dbCommands(f"update `user` set `language`='{user.language}' where `user_id`='{user.hash_id}'")
        await bot.send_message(user.id, localization.choosed_language[user.language])
        return
    elif callback_query.data == "default_gpt" or callback_query.data == "ukrainisation_gpt":
        user.GPT_type = callback_query.data
        database.dbCommands(f"update `user` set `gpt_type`='{user.GPT_type}' where `user_id`='{user.hash_id}'")
        return


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
