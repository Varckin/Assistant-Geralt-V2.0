from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


base_router = Router()

@base_router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hello")


@base_router.message(Command("info"))
async def cmd_info( message:Message):

    text: str = f'''
/weather - shows the current weather.
/tat2rus - translate tatar to russian.
/rus2tat - translate russian to tatar.
/translate - translate word or or proposal.
/change_language - change language translate.
/generator - generator passcode.
/gallows - game gallows.
/anonim_mail - random anonim email.
/help - displays information about commands.
/about - displays information about the bot.
/cancel - Cancel all commands
'''
    await message.answer(text=text)
