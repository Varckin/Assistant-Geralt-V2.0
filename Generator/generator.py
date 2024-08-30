from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import random
import string


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
async def cmd_start(message: Message, state: FSMContext):
    text = '''
Enter the parameters in the following message.
l - use lower case.
u - use upper case.
d - use numbers.
s - use special characters.
For example: ld 8(password length)
'''
    await message.answer(text=text)
    await state.set_state(GeneratorState.generatorstate)


@generator_router.message(GeneratorState.generatorstate)
async def process_source_language(message: Message, state: FSMContext):
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
            password = gen.generate_password(length=length, use_lower=l, use_upper=u, use_digits=d, use_special=s)
            await message.answer(text=password)
        else:
            await message.answer(text='Reread the team instructions.')
    except (ValueError, IndexError):
        await message.answer(text='Reread the team instructions.')
        