from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from pathlib import Path
from random import choice
from io import BufferedReader


gallows_router = Router()


class GallowsState(StatesGroup):
    gallowsState = State()


class Gallows():
    def __init__(self):
        self.tries: int = 8
    def list_words(self) -> list:
        with open(f'{str(Path.cwd())}/Gallows/words.txt', 'r', encoding='utf-8') as file:
            list_words: list = file.read().split()
            return list_words

    def gif_load(self) -> BufferedReader:
        with open(f'{str(Path.cwd())}/Gallows/gallows_lose.gif', 'rb') as file:
            return file
    
    def choice_word(self) -> str:
        return choice(self.list_words()).lower()


@gallows_router.message(Command("gallows"))
async def cmd_gallows (message: Message, state: FSMContext):
    gall: Gallows = Gallows()
    tries: int = gall.tries
    selected_word: str = choice(gall.choice_word).lower()
    guessed_letters: list = []
    guessed_word: str = ''.join('*' if letter not in guessed_letters else letter for letter in selected_word)

    await state.update_data(
        selected_word=selected_word,
        guessed_word=guessed_word,
        guessed_letters=guessed_letters,
        tries=tries
    )
    await state.set_state(GallowsState.gallowsState)

    text: str = f'''
The word is selected. Write the letter.
Guessed word: {guessed_word}
Tries: {tries}
'''
    await message.answer(text=text)


@gallows_router.message(GallowsState.gallowsState)
async def game_run(message: Message, state: FSMContext):
    gall: Gallows = Gallows()
    data: dict = await state.get_data()
    selected_word: str = data['selected_word']
    guessed_letters: list = data['guessed_letters']
    guessed_word: str = data['guessed_word']
    tries: int = data['tries']

    guess = message.text.lower()

    if len(guess) != 1:
        await message.reply(f"Please enter only one letter.\n"
                           f"Guessed word: {guessed_word}")
        return

    if guess in guessed_letters:
        await message.reply(f"You have already guessed this letter.\n"
                           f"Guessed word: {guessed_word}")
        return
    
    if guess in selected_word:
        guessed_letters.append(guess)
        guessed_word = ''.join(letter if letter in guessed_letters else '*' for letter in selected_word)

        if guessed_word == selected_word:
            await message.reply(f"Congratulations! You've won!\n"
                               f"Guessed word: {guessed_word}")
            await state.finish()
        else:
            await message.reply(f"Right!\n"
                               f"Guessed word: {guessed_word}")
    else:
        tries -= 1

        if tries == 0:
            await message.reply(f"You've lost! The hidden word was: {selected_word}")
            await message.answer_animation(animation=gall.gif_load())
            await state.finish()
        else:
            await message.reply(f"Wrong!\n"
                               f"Guessed word: {guessed_word}\n"
                               f"Tries: {tries}")

    await state.update_data(
        guessed_word=guessed_word,
        guessed_letters=guessed_letters,
        tries=tries
    )
