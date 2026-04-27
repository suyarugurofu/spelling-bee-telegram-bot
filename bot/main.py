from bot.config import Config
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.enums import ParseMode
from bot.handlers import router as handlers_router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not Config.BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в .env")

bot = Bot(token=Config.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
dp.include_router(handlers_router)

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать")
    ]
    await bot.set_my_commands(commands)

async def main():
    logger.info("The bot has been launched...")
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
