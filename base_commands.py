from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from pathlib import Path
from json_def import json_read
from Localization.localization import getStr


base_router = Router()


@base_router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(text=getStr(lang_code=message.from_user.language_code,
                                      key_str="start_welcome").format(first_name=message.chat.first_name))


@base_router.message(Command("info"))
async def cmd_info( message: Message):
    await message.answer(text=getStr(lang_code=message.from_user.language_code,
                                      key_str="info"))


@base_router.message(Command("about"))
async def cmd_about(message: Message):
    version: str = json_read(f'{str(Path.cwd())}/res/config.json')["version"]
    await message.answer(text=getStr(lang_code=message.from_user.language_code,
                                      key_str="about").format(version=version),
                                      parse_mode='Markdown')


@base_router.message(Command("bonus_math"))
async def cmd_bonus_math(message: Message):
    list_parm: list = message.text.split()
    if len(list_parm) == 2:
        cmd, num = list_parm
        try:
            num: int = int(num)
            text: str = getStr(lang_code=message.from_user.language_code, key_str="bonusMath")
            await message.answer(text=f"{text} {num * 7.6 / 100}")
        except ValueError:
            await message.answer(text=getStr(lang_code=message.from_user.language_code,
                                             key_str="error"))
    else: await message.answer(text=getStr(lang_code=message.from_user.language_code,
                                           key_str="error"))


@base_router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(text=getStr(lang_code=message.from_user.language_code,
                                         key_str="cancelNoState"),
                                         reply_markup=ReplyKeyboardRemove())
    else:
        await state.clear()
        await message.answer(text=getStr(lang_code=message.from_user.language_code,
                                         key_str="cancelOperationCanceled"),
                                         reply_markup=ReplyKeyboardRemove())
