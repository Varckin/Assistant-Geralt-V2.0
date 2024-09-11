from json_def import json_read
from pathlib import Path
import json
import requests
import logging
from logger import config_log
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


logger = logging.getLogger('shortlink')
logger.setLevel(logging.INFO)
logger.addHandler(config_log.command_logger)


shortlink_router = Router()
        
    
class Shortlink():
    def __init__(self):
        self.base_url: str = json_read(f'{str(Path.cwd())}/res/config.json')['short_link_url']
        self.token: str = json_read(f'{str(Path.cwd())}/res/config.json')['token_short_link']
    
    def create_link(self, long_url: str) -> dict:
        self.create_url: str = "create"
        payload: dict = {
            "url": long_url
        }
        headers: dict = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(url=self.base_url+self.create_url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                json_response: dict = response.json()
                return json_response.get("data")
            else:
                return {"tiny_url": "error"}
        except Exception as e:
            logger.error(f"Error: {e}")


@shortlink_router.message(Command("shortlink"))
async def cmd_shortlink( message:Message):
    list_message: list = message.text.split()
    if len(list_message) == 2:
        shrt = Shortlink()
        response: dict = shrt.create_link(list_message[1])
        text: str = f"""
Длинная ссылка: {response.get("url")}
Короткая ссылка: {response.get("tiny_url")}
"""
        await message.reply(text=text)
    else:
        await message.answer(text="Введите правильную структуру сообщения.")
