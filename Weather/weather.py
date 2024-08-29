from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from urllib.parse import quote

import requests

from json_def import json_read
from base_def import current_directory


weather_router = Router()


class Weather():
    def weather(self, city: str, lang: str = 'en'):
        self.city = quote(city)
        self.url: str = f'{json_read(f'{current_directory()}/res/config.json')['weather_url']}/{city}?format=j2&lang={lang}'
        self.response = requests.get(self.url)
        if self.response.status_code == 200:
            self.data: dict = self.response.json()
            self.text: str = ''
            for day in self.data['weather']:
                text = f'''
City:
Date: {day['date']}
Temperature: {day['avgtempC']}
'''
                self.text += text
            return self.text


@weather_router.message(Command("weather"))
async def cmd_info( message:Message):
    cmd, city = message.text.split()
    await message.answer(text=Weather().weather(city))
