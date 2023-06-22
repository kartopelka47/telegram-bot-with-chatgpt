import aiogram


def get_language_menu():
    markup_of_lang_buttons = aiogram.types.inline_keyboard.InlineKeyboardMarkup(row_width=1)
    ua_language = aiogram.types.inline_keyboard.InlineKeyboardButton("🇺🇦Українська",callback_data="uk")
    en_language = aiogram.types.inline_keyboard.InlineKeyboardButton("🇬🇧English",callback_data="en")
    markup_of_lang_buttons.add(ua_language,en_language)
    return markup_of_lang_buttons
