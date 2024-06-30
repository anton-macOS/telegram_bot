import os
from telegram_bot.logger_setup import logger
from dotenv import load_dotenv

import asyncio

from aiogram import Bot, Dispatcher

from handlers.main_handlers import main_handler
from handlers.admin_handler import admin_handler
from admin_management import admin_management
from handlers.team_lead_handler import team_lead
from team_lead_management import team_lead_management
from handlers.mentor_handler import mentor_handler
from mentor_management import mentor_management

from db.session import engine
from models.user import Base


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(main_handler)
    dp.include_router(admin_handler)
    dp.include_router(admin_management)
    dp.include_router(team_lead)
    dp.include_router(team_lead_management)
    dp.include_router(mentor_handler)
    dp.include_router(mentor_management)
    await dp.start_polling(bot)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    logger.info('Starting bot...')
    asyncio.run(main())
