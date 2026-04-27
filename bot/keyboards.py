from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.i18n import PHRASES

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=PHRASES["menu_start"])],
            [KeyboardButton(text=PHRASES["menu_stats"])],
            [KeyboardButton(text=PHRASES["menu_accent"])],
            [KeyboardButton(text=PHRASES["menu_change_level"])]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def level_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=PHRASES["level_easy"])],
            [KeyboardButton(text=PHRASES["level_medium"])],
            [KeyboardButton(text=PHRASES["level_hard"])]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def training_actions():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=PHRASES["menu_next_word"])],
            [KeyboardButton(text=PHRASES["menu_finish_training"])]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def accent_menu():
    buttons = [
        [KeyboardButton(text=PHRASES["accent_usa"])],
        [KeyboardButton(text=PHRASES["accent_uk"])],
        [KeyboardButton(text=PHRASES["accent_australia"])],
        [KeyboardButton(text=PHRASES["accent_canada"])],
        [KeyboardButton(text=PHRASES["accent_india"])]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)