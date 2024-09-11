import asyncio
import logging
from aiogram import Bot, Dispatcher
from pathlib import Path

from base_commands import base_router
from Translate.translate import translate_router
from Weather.weather import weather_router
from Generator.generator import generator_router
from AnonimMail.anonim_mail import anonim_mail_router
from Gallows.gallows import gallows_router
from YesOrNo.yesorno import yesorno_router
from Reminder.reminder import reminder_router
from ShortLink.shortlink import shortlink_router
from json_def import json_read
from logger import config_log

logger = logging.getLogger('main')
logger.setLevel(logging.INFO)
logger.addHandler(config_log.bot_logger)


async def main():
    token: str = json_read(f'{str(Path.cwd())}/res/config.json')["telegram_token"]
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(base_router)
    dp.include_router(translate_router)
    dp.include_router(weather_router)
    dp.include_router(generator_router)
    dp.include_router(anonim_mail_router)
    dp.include_router(gallows_router)
    dp.include_router(yesorno_router)
    dp.include_router(reminder_router)
    dp.include_router(shortlink_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        logger.info('Start bot.')
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Bot Error: {e}")
