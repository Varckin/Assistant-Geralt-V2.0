import asyncio
import sys
import logging
from aiogram import Bot, Dispatcher

from base_commands import base_router
from Translate.translate import translate_router
from Weather.weather import weather_router
from json_def import json_read
from base_def import current_directory


logging.basicConfig(
    filename=f'{current_directory()}/log/bot.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


async def main():
    token: str = json_read(f'{current_directory()}/res/config.json')["telegram_token"]
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(base_router)
    dp.include_router(translate_router)
    dp.include_router(weather_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
