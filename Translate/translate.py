import requests
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from urllib.parse import quote
from json_def import json_read
from base_def import current_directory


translate_router = Router()


class Translate():

    def translate(self, source_language: str, destination_language: str, sentence_for_translation: str):
        encoded_text = quote(sentence_for_translation)
        self.base_url: str = 'https://ftapi.pythonanywhere.com/'
        self.translate_url: str = f'translate?sl={source_language}&dl={destination_language}&text={encoded_text}'
        response = requests.get(self.base_url+self.translate_url)
        if response.status_code == 200:
            data: dict = response.json()
            text: str = f'''
"sl": {data['source-language']}
"st": {data['source-text']}
"dl": {data['destination-language']}
"dt": {data['destination-text']}
'''
            return text
        else:
            print(f"Ошибка: {response.status_code}")

    def select_lang(self):
        lang: dict = json_read(f'{current_directory()}/Translate/lang_available.json')
        return lang
    

class TranslationState(StatesGroup):
    first_land = State()
    second_lang = State()
    input_text = State()


def lang_keyboard(buttons_per_row: int = 3) -> ReplyKeyboardMarkup:
    buttons = [KeyboardButton(text=lang_name) for lang_name in Translate().select_lang().values()]
    keyboard = [buttons[i:i + buttons_per_row] for i in range(0, len(buttons), buttons_per_row)]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


@translate_router.message(Command("translate"))
async def cmd_info( message:Message, state: FSMContext):
    await message.answer(text='Enter lang', reply_markup=lang_keyboard())
    await state.set_state(TranslationState.first_land)


@translate_router.message(TranslationState.first_land)
async def process_source_language(message: Message, state: FSMContext):
    lang: dict = Translate().select_lang()
    first_language: str = next((lang_code for lang_code, lang_name in lang.items() if lang_name in message.text), None)
    
    if first_language:
        await state.update_data(first_language=first_language)
        await message.answer("Теперь выбери целевой язык перевода:", reply_markup=lang_keyboard())
        await state.set_state(TranslationState.second_lang)
    else:
        await message.answer("Пожалуйста, выбери язык, используя кнопки.")


@translate_router.message(TranslationState.second_lang)
async def process_source_language(message: Message, state: FSMContext):
    lang: dict = Translate().select_lang()
    second_language: str = next((lang_code for lang_code, lang_name in lang.items() if lang_name in message.text), None)
    
    if second_language:
        await state.update_data(second_language=second_language)
        await message.answer("Теперь выбери целевой язык перевода:", reply_markup=lang_keyboard())
        await state.set_state(TranslationState.input_text)
    else:
        await message.answer("Пожалуйста, выбери язык, используя кнопки.")


@translate_router.message(TranslationState.input_text)
async def process_input_text(message: Message, state: FSMContext):
    lang = Translate()
    user_data: dict = await state.get_data()
    first_language: str = user_data['first_language']
    second_language: str = user_data['second_language']
    text_to_translate: str = message.text

    await message.answer(text=lang.translate(first_language, second_language, text_to_translate))
