from aiogram import Router, F
from aiogram.types import Message
from bot.database import execute
from bot.keyboards import main_menu, level_menu
from bot.i18n import PHRASES

router = Router()

@router.message(F.text.startswith("/start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    await execute("INSERT INTO users (id) VALUES ($1) ON CONFLICT DO NOTHING", user_id)
    await message.answer(PHRASES["start_welcome"], reply_markup=level_menu())

@router.message(F.text.in_(PHRASES["level_options"]))
async def set_level(message: Message):
    user_id = message.from_user.id
    level_map = {
        PHRASES["level_easy"]: 1,
        PHRASES["level_medium"]: 2,
        PHRASES["level_hard"]: 3
    }
    level = level_map[message.text]
    await execute("UPDATE users SET training_level = $1 WHERE id = $2", level, user_id)
    response = PHRASES["level_set"].format(level=message.text)
    await message.answer(response, reply_markup=main_menu())

@router.message(F.text == PHRASES["menu_change_level"])
async def change_level(message: Message):
    await message.answer(PHRASES["change_level_prompt"], reply_markup=level_menu())