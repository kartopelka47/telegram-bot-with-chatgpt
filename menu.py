from aiogram import types

import config
import localization


def get_language_menu() -> types.inline_keyboard.InlineKeyboardMarkup:
    """
    :return: InlineKeyboardMarkup with language buttons
    """
    markup_of_lang_buttons = types.inline_keyboard.InlineKeyboardMarkup(row_width=1)
    ua_language = types.inline_keyboard.InlineKeyboardButton("🇺🇦Українська",callback_data="uk")
    en_language = types.inline_keyboard.InlineKeyboardButton("🇬🇧English",callback_data="en")
    markup_of_lang_buttons.add(ua_language,en_language)
    return markup_of_lang_buttons


def user_from_tgUrl(language,url) -> types.inline_keyboard.InlineKeyboardMarkup:
    """
    :type language: str
    :type url: str
    :return: button with a link to the user
    """
    markup = types.inline_keyboard.InlineKeyboardMarkup(row_width=1)
    user_button = types.inline_keyboard.InlineKeyboardButton(localization.user[language], url=url)
    markup.add(user_button)
    return markup


def change_bot_type(language) -> types.inline_keyboard.InlineKeyboardMarkup:
    """
    :type language: str
    """
    markup = types.inline_keyboard.InlineKeyboardMarkup(row_width=1)
    default_gpt = types.inline_keyboard.InlineKeyboardButton(localization.default[language],
                                                             callback_data="default_gpt")
    ukrainisation = types.inline_keyboard.InlineKeyboardButton(localization.ukrainisation[language],
                                                               callback_data="ukrainisation_gpt")
    markup.add(default_gpt, ukrainisation)
    return markup


def payment_help_button(language) -> types.inline_keyboard.InlineKeyboardMarkup:
    """
    :type language: str
    """
    markup = types.inline_keyboard.InlineKeyboardMarkup(row_width=1)
    payment_button = types.inline_keyboard.InlineKeyboardButton(localization.help_translate[language],
                                                                url=config.PAYMENT_LINK)
    markup.add(payment_button)
    return markup


def cancel_button() -> types.reply_keyboard.ReplyKeyboardMarkup:
    markup = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    cancel = types.reply_keyboard.KeyboardButton("/cancel")
    markup.add(cancel)
    return markup

