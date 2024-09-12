from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import random
import string

import logging
from logger import config_log
from Localization.localization import getStr


logger = logging.getLogger('generator')
logger.setLevel(logging.INFO)
logger.addHandler(config_log.command_logger)


generator_router = Router()


class GeneratorState(StatesGroup):
    generatorstate = State()


class Generator():
    def generate_password(self, length: int, use_lower:bool, use_upper: bool, use_digits: bool, use_special: bool) -> str:
        characters: str = ''

        if use_lower:
            characters += string.ascii_lowercase
        if use_upper:
            characters += string.ascii_uppercase
        if use_digits:
            characters += string.digits
        if use_special:
            characters += string.punctuation

        return ''.join(random.choice(characters) for _ in range(length))


@generator_router.message(Command("generator"))
async def cmd_generator(message: Message, state: FSMContext):
    text: str = getStr(lang_code=message.from_user.language_code, key_str="generatorInstructions")
    await message.answer(text=text)
    await state.set_state(GeneratorState.generatorstate)


@generator_router.message(GeneratorState.generatorstate)
async def process_generator(message: Message, state: FSMContext):
    try:
        gen = Generator()
        param, length = message.text.split()
        length = int(length)
        param = param.lower()
        
        l: bool = 'l' in param
        u: bool = 'u' in param
        d: bool = 'd' in param
        s: bool = 's' in param

        if len(param) <= 4 and (l or u or d or s):
            password: str = gen.generate_password(length=length, use_lower=l, use_upper=u, use_digits=d, use_special=s)
            await message.answer(text=password)
        else:
            await message.answer(text=getStr(lang_code=message.from_user.language_code, key_str="error"))
    except (ValueError, IndexError)as e:
        await message.answer(text=getStr(lang_code=message.from_user.language_code, key_str="error"))
        logger.error(f'Error value or index: {e}')
        