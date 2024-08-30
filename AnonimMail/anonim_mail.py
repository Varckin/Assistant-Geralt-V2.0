from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

import requests


anonim_mail_router = Router()


class AnonimMailState(StatesGroup):
    AnonimMailState = State()


class AnonimMail():
    def __init__(self):
        self.base_url: str = 'https://www.1secmail.com/api/v1/'
    def random_generation_email(self):
        self.random_gen_url: str = f'{self.base_url}?action=genRandomMailbox'
        response = requests.get(self.base_url+self.random_gen_url)
        if response.status_code == 200:
            data: dict = response.json()
            return data[0]
    def check_email(self, login: str, domain: str):
        self.check_email_url: str = f'{self.base_url}?action=getMessages&login={login}&domain={domain}'
        response = requests.get(self.base_url+self.check_email_url)
        if response.status_code == 200:
            data: dict = response.json()
            text: str = 'Your messages:'
            if not data:
                text += '\nNot message in emailbox'
                return text
            else:
                for mail in data:
                    email_id, email_from, email_subject, email_date = mail["id"], mail["from"], mail["subject"], mail["date"]
                    text += f'''
id mail: {email_id}
from: {email_from}
subject:{email_subject}
date: {email_date}
'''
                return text


@anonim_mail_router.message(Command("anonim_mail"))
async def cmd_anonim_mail(message: Message, state: FSMContext):
    anonim = AnonimMail()
    await state.set_state(AnonimMailState.AnonimMailState)
    but_check = InlineKeyboardButton(text='Refresh', callback_data='press_check')
    but_change = InlineKeyboardButton(text='Change email', callback_data='press_change')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [but_check],
        [but_change]
        ])
    email: str = anonim.random_generation_email()
    login, domain = email.split('@')
    await state.update_data(login=login, domain=domain)
    
    await message.answer(text=f'Your email: {email}', reply_markup=keyboard)


@anonim_mail_router.callback_query(lambda c: c.data == 'press_check')
async def press_check(callback_query: CallbackQuery, state: FSMContext):
    anonim = AnonimMail()
    email_data: dict = await state.get_data()
    text = anonim.check_email(login=email_data['login'], domain=email_data['domain'])
    await callback_query.message.edit_text(text=text, reply_markup=callback_query.message.reply_markup)
    await callback_query.answer()


@anonim_mail_router.callback_query(lambda c: c.data == 'press_change')
async def press_check(callback_query: CallbackQuery, state: FSMContext):
    anonim = AnonimMail()
    email: str = anonim.random_generation_email()
    login, domain = email.split('@')
    await state.update_data(login=login, domain=domain)
    await callback_query.message.edit_text(text=f'Your email: {email}', reply_markup=callback_query.message.reply_markup)
    await callback_query.answer()
    