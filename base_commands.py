from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from pathlib import Path
from json_def import json_read


base_router = Router()

@base_router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(f"Hello {message.chat.first_name}")


@base_router.message(Command("info"))
async def cmd_info( message: Message):
    text: str = f'''
/weather - shows the current weather.
/translate - translate word or or proposal.
/generator - generator passcode.
/gallows - game gallows.
/anonim_mail - random anonim email.
/bonus_math - Salary calculation.
/yesorno - Heads and tails.
/reminder - The team will create notes for you.
/info - displays information about commands.
/about - displays information about the bot.
/cancel - Cancel all commands
'''
    await message.answer(text=text)


@base_router.message(Command("about"))
async def cmd_about(message: Message):
    version: str = json_read(f'{str(Path.cwd())}/res/config.json')["version"]
    text: str = f'''
Creater: [Markus](t.me/varckin)
Version: {version}
'''
    await message.answer(text=text, parse_mode='Markdown')


@base_router.message(Command("bonus_math"))
async def cmd_bonus_math(message: Message):
    list_parm: list = message.text.split()
    if len(list_parm) == 2:
        cmd, num = list_parm
        try:
            num: int = int(num)
            await message.answer(text=f"Твои расчеты: {num * 7.6 / 100}")
        except ValueError:
            await message.answer(text='Введите цифру.')
    else: await message.answer(text='Введите понятное дело.')


@base_router.message(Command("cancel"))
async def cmd_canscl(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(text='No active state')
    else:
        await state.clear()
        await message.answer(text='Operation canceled.', reply_markup=ReplyKeyboardRemove())
