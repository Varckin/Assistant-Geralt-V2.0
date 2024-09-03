from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

import requests
import io
import logging
from logger import config_log
from json_def import json_read
from pathlib import Path


logger = logging.getLogger('anonim_mail')
logger.setLevel(logging.INFO)
logger.addHandler(config_log.command_logger)


anonim_mail_router = Router()


class AnonimMailState(StatesGroup):
    anonimMailState = State()


class AnonimMail():
    def __init__(self):
        self.base_url: str = json_read(f'{str(Path.cwd())}/res/config.json')['anonim_mail_url']
    def random_generation_email(self):
        self.random_gen_url: str = '?action=genRandomMailbox'
        response = requests.get(self.base_url+self.random_gen_url)
        try:
            if response.status_code == 200:
                data: dict = response.json()
                return data[0]
        except IndexError as e:
            logger.error(f'Index error: {e}')
    def check_email(self, login: str, domain: str):
        self.check_email_url: str = f'?action=getMessages&login={login}&domain={domain}'
        response = requests.get(self.base_url+self.check_email_url)
        try:
            if response.status_code == 200:
                data: dict = response.json()
                text: str = f'{login}@{domain}\nYour messages:'
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
        except KeyError as e:
            logger.error(f'Key error: {e}')
        except Exception as e:
            logger.error(f'Error: {e}')
    def fetching_message(self, login: str, domain: str, id_message: str):
        self.fetching_message_url: str = f'?action=readMessage&login={login}&domain={domain}&id={id_message}'
        response = requests.get(self.base_url+self.fetching_message_url)
        try:
            if response.status_code == 200:
                data: dict = response.json()
                print(data)
                id_mess, from_mail, subject, date, attachments, textbody = (
                    data['id'],
                    data['from'],
                    data['subject'],
                    data['date'],
                    data['attachments'],
                    data['textBody']
                    )
                text_attach: str = ''
                if not attachments:
                    pass
                else:
                    for attachment in attachments:
                        filename: str = attachment['filename']
                        size: str = str(attachment['size'])
                        text_attach += filename
                        text_attach += size
                text: str = f'''
        "id": {str(id_mess)}
        "from": {from_mail}
        "subject": {subject}
        "date": {date}
        "attachments": {text_attach}
        "textBody": {textbody}
    '''
                return text
        except KeyError as e:
            logger.error(f'Key error: {e}')
        except Exception as e:
            logger.error(f'Error: {e}')
    def attachment_download (self, login: str, domain: str, id_message: str, file_name: str):
        self.attachment_download_url = f'?action=download&login={login}&domain={domain}&id={id_message}&file={file_name}'
        response = requests.get(self.base_url+self.fetching_message_url)
        try:
            if response.status_code == 200:
                file_attachment = io.BytesIO(response.content)
                file_attachment.name = file_name

                return file_attachment
        except Exception as e:
            logger.error(f'Error: {e}')


@anonim_mail_router.message(Command("anonim_mail"))
async def cmd_anonim_mail(message: Message, state: FSMContext):
    anonim = AnonimMail()
    try:
        await state.set_state(AnonimMailState.anonimMailState)
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
    except Exception as e:
        logger.error(f'Error: {e}')


@anonim_mail_router.callback_query(lambda c: c.data == 'press_check')
async def press_check(callback_query: CallbackQuery, state: FSMContext):
    anonim = AnonimMail()
    try:
        email_data: dict = await state.get_data()
        text = anonim.check_email(login=email_data['login'], domain=email_data['domain'])
        await callback_query.message.edit_text(text=text, reply_markup=callback_query.message.reply_markup)
        await callback_query.answer()
    except Exception as e:
        logger.error(f'Error: {e}')


@anonim_mail_router.callback_query(lambda c: c.data == 'press_change')
async def press_check(callback_query: CallbackQuery, state: FSMContext):
    anonim = AnonimMail()
    try:
        email: str = anonim.random_generation_email()
        login, domain = email.split('@')
        await state.update_data(login=login, domain=domain)
        await callback_query.message.edit_text(text=f'Your email: {email}', reply_markup=callback_query.message.reply_markup)
        await callback_query.answer()
    except Exception as e:
        logger.error(f'Error: {e}')
    

@anonim_mail_router.message(AnonimMailState.anonimMailState)
async def catch_id_and_attachments(message: Message, state: FSMContext):
    anonim = AnonimMail()
    email_data: dict = await state.get_data()
    parm: list = message.text.split()
    try:
        if len(parm) == 2:
            cmd, id_mess = parm
        elif len(parm) == 3:
            cmd, id_mess, attachment = parm
        else:
            await message.answer(text='Введите правильно параметры.')
            return
        
        if isinstance(int(id_mess), int):
            if cmd == 'id':
                await message.reply(text=anonim.fetching_message(login=email_data['login'], domain=email_data['domain'], id_message=id_mess))
            elif cmd == 'attachment':
                await message.reply_document(document=anonim.attachment_download(login=email_data['login'], domain=email_data['domain'], id_message=id_mess, file_name=attachment))
            else:
                await message.answer(text='Что то не так. проверьте правильность данных')
                return
    except Exception as e:
        logger.error(f'Error: {e}')
