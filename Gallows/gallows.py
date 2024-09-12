from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from pathlib import Path
from random import choice
import logging
from logger import config_log
from Localization.localization import getStr


logger = logging.getLogger('gallows')
logger.setLevel(logging.INFO)
logger.addHandler(config_log.command_logger)


gallows_router = Router()


class GallowsState(StatesGroup):
    gallowsState = State()


class Gallows():
    def __init__(self):
        self.tries: int = 8
    def list_words(self) -> list:
        try:
            with open(f'{str(Path.cwd())}/Gallows/words.txt', 'r', encoding='utf-8') as file:
                list_words: list = file.read().split()
                return list_words
        except FileNotFoundError as e:
            logger.error(f'File not found: {e}')
        except PermissionError as e:
            logger.error(f'No permission: {e}')

    def gif_load(self) -> str:
        try:
            return f'{str(Path.cwd())}/Gallows/gallows_lose.gif'
        except ValueError as e:
            logger.error(f'Value error: {e}')
    
    def choice_word(self) -> str:
        return choice(self.list_words()).lower()


@gallows_router.message(Command("gallows"))
async def cmd_gallows (message: Message, state: FSMContext):
    gall = Gallows()
    tries: int = gall.tries
    selected_word: str = gall.choice_word()
    guessed_letters: list = []
    guessed_word: str = ''.join('*' if letter not in guessed_letters else letter for letter in selected_word)

    await state.update_data(
        selected_word=selected_word,
        guessed_word=guessed_word,
        guessed_letters=guessed_letters,
        tries=tries
    )
    await state.set_state(GallowsState.gallowsState)
    text: str = getStr(lang_code=message.from_user.language_code, key_str="gallowWordSelected").format(guessed_word=guessed_word, tries=tries)
    await message.answer(text=text)


@gallows_router.message(GallowsState.gallowsState)
async def game_run(message: Message, state: FSMContext):
    gall = Gallows()
    data: dict = await state.get_data()
    selected_word: str = data['selected_word']
    guessed_letters: list = data['guessed_letters']
    guessed_word: str = data['guessed_word']
    tries: int = data['tries']

    guess = message.text.lower()
    try:
        if len(guess) != 1:
            await message.reply(getStr(lang_code=message.from_user.language_code, key_str="gallowEnterOneLetter").format(guessed_word=guessed_word))
            return

        if guess in guessed_letters:
            await message.reply(getStr(lang_code=message.from_user.language_code, key_str="gallowAlreadyLetter").format(guessed_word=guessed_word))
            return
        
        if guess in selected_word:
            guessed_letters.append(guess)
            guessed_word = ''.join(letter if letter in guessed_letters else '*' for letter in selected_word)

            if guessed_word == selected_word:
                await message.reply(getStr(lang_code=message.from_user.language_code, key_str="gallowCongratulation").format(guessed_word=guessed_word))
                await state.clear()
            else:
                await message.reply(getStr(lang_code=message.from_user.language_code, key_str="gallowRight").format(guessed_word=guessed_word))
        else:
            tries -= 1

            if tries == 0:
                await message.reply(getStr(lang_code=message.from_user.language_code, key_str="gallowLost").format(selected_word=selected_word))
                gif = FSInputFile(gall.gif_load())
                await message.answer_animation(animation=gif)
                await state.clear()
            else:
                await message.reply(getStr(lang_code=message.from_user.language_code, key_str="gallowWrong").format(guessed_word=guessed_word, tries=tries))

        await state.update_data(
            guessed_word=guessed_word,
            guessed_letters=guessed_letters,
            tries=tries
        )
    except FileNotFoundError as e:
        logger.error(f'File not found: {e}')
    except PermissionError as e:
        logger.error(f'No permission: {e}')
    except Exception as e:
        logger.error(f'Error: {e}')
