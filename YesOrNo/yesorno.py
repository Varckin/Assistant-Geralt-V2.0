from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import requests
from requests.exceptions import RequestException
from json_def import json_read
from pathlib import Path
import logging
from logger import config_log


logger = logging.getLogger('yesorno')
logger.setLevel(logging.INFO)
logger.addHandler(config_log.command_logger)


yesorno_router = Router()


def get_answer_big_questions():
        url: str = json_read(f'{str(Path.cwd())}/res/config.json')["yesorno_url"]
        response = requests.get(url)
        try:
            if response.status_code == 200:
                try:
                    data: dict = response.json()
                    return data['image']
                except KeyError as e:
                    logger.error(f"Key image not find: {e}")
                except ValueError as e:
                    logger.error(f"Error decode JSON: {e}")
            else:
                response.raise_for_status()
        except RequestException as e:
             logger.info(f"response status code not 200: {str(e)}")
        except Exception as e:
             logger.info(f"Error: {e}")


@yesorno_router.message(Command("yesorno"))
async def cmd_gallows (message: Message):
    await message.answer_animation(animation=get_answer_big_questions())
