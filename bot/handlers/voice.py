from aiogram import Router, F
from aiogram.types import Message
from bot.database import execute
from bot.keyboards import main_menu, accent_menu
from bot.i18n import PHRASES

router = Router()

@router.message(F.text == PHRASES["menu_accent"])
async def choose_accent(message: Message):
    await message.answer(PHRASES["choose_accent"], reply_markup=accent_menu())

@router.message(F.text.in_([
    PHRASES["accent_usa"],
    PHRASES["accent_uk"],
    PHRASES["accent_australia"],
    PHRASES["accent_canada"],
    PHRASES["accent_india"]
]))
async def set_accent(message: Message):
    accent_map = {
        PHRASES["accent_usa"]: "com",
        PHRASES["accent_uk"]: "co.uk",
        PHRASES["accent_australia"]: "com.au",
        PHRASES["accent_canada"]: "ca",
        PHRASES["accent_india"]: "co.in"
    }
    accent_code = accent_map[message.text]
    user_id = message.from_user.id
    await execute("UPDATE users SET tts_accent = $1 WHERE id = $2", accent_code, user_id)
    response = PHRASES["accent_set"].format(accent=message.text)
    await message.answer(response, reply_markup=main_menu())