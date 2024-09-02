from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import requests


yesorno_router = Router()


def get_answer_big_questions():
        url: str = 'https://yesno.wtf/api'
        response = requests.get(url)
        if response.status_code == 200:
            data: dict = response.json()
            return data['image']


@yesorno_router.message(Command("yesorno"))
async def cmd_gallows (message: Message):
    await message.answer_animation(animation=get_answer_big_questions())
