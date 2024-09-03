from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from urllib.parse import quote

import requests
from requests.exceptions import RequestException
from pathlib import Path
from json_def import json_read
import logging
from logger import config_log


logger = logging.getLogger('weather')
logger.setLevel(logging.INFO)
logger.addHandler(config_log.command_logger)


weather_router = Router()


class Weather():
    def weather(self, city: str, lang: str = 'en'):
        try:
            self.city = quote(city)
            self.directory = json_read(f'{str(Path.cwd())}/res/config.json')['weather_url']
            self.url: str = f'{self.directory}/{city}?format=j2&lang={lang}'
            self.response = requests.get(self.url)
            if self.response.status_code == 200:
                self.data: dict = self.response.json()
                self.text: str = ''
                self.city: list = []
                for area in self.data['nearest_area']:
                    for key in area:
                        if key == 'weatherUrl':
                            continue
                        for item in area[key]:
                            if 'value' in item:
                                self.city.append(item['value'])
                self.text += f'City: {self.city[1]}, {self.city[2]}, {self.city[0]}'
                for day in self.data['weather']:
                    text = f'''
Date: {day['date']}
Approximate temperature: {day['avgtempC']}
'''
                    self.text += text
                return self.text
            self.response.raise_for_status()
        except IndexError as e:
            logger.error(f'Index error: {e}')
        except KeyError as e:
            logger.error(f'Key error: {e}')
        except RequestException as e:
            logger.info(f'Status code not 200: {e}')
        except Exception as e:
            logger.error(f'Error: {e}')


@weather_router.message(Command("weather"))
async def cmd_info( message:Message):
    try:
        cmd, city = message.text.split()
        await message.answer(text=Weather().weather(city))
    except:
        await message.answer(text='Enter normal request')
