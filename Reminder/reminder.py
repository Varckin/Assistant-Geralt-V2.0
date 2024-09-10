from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from pathlib import Path
import logging
import json
from json_def import json_read, json_write
from logger import config_log
from uuid import uuid4
from datetime import datetime

logger = logging.getLogger('reminder')
logger.setLevel(logging.INFO)
logger.addHandler(config_log.command_logger)


reminder_router = Router()


class ReminderState(StatesGroup):
    reminderstate = State()
    createstate = State()
    deletestate = State()

def reminder_keyboard() -> ReplyKeyboardMarkup:
    show_reminder = KeyboardButton(text="Показать напоминания")
    create_reminder = KeyboardButton(text="Создать напоминание")
    delete_reminder = KeyboardButton(text="Удалить напоминание")
    keyboard: list = [[show_reminder], [create_reminder], [delete_reminder]]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


class Reminder():
    def create_reminder(self, id_user: str, description: str):
        uuid = str(uuid4())
        reminder: dict = {
             uuid: {
            "id": uuid,
            "description": description,
            "id_user": id_user,
            "created_at": datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
             }
        }

        try:
            reminders: dict = json_read(file_name=f"{str(Path.cwd())}/Reminder/reminders.json")            
            reminders.update(reminder)
            json_write(file_name=f"{str(Path.cwd())}/Reminder/reminders.json", dict=reminders)
            
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except KeyError as e:
            logger.error(f"Key error: {e}")
    
    def show_reminder(self, id_user: str):
        user_reminder: dict = {}
        try:
            reminders: dict = json_read(file_name=f"{str(Path.cwd())}/Reminder/reminders.json")    

            for key, item in reminders.items():
                if item["id_user"] == id_user:
                    user_reminder[key] = item

            return user_reminder
           
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except KeyError as e:
            logger.error(f"Key error: {e}")

    def delete_reminders(self, uuid: str) -> bool:
        try:
            reminders: dict = json_read(file_name=f"{str(Path.cwd())}/Reminder/reminders.json")   
            
            if uuid in reminders:
                del reminders[uuid]
                json_write(file_name=f"{str(Path.cwd())}/Reminder/reminders.json", dict=reminders)
                return True
            else:
                return False
           
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            return False
        except KeyError as e:
            logger.error(f"Key error: {e}")
            return False


@reminder_router.message(Command("reminder"))
async def cmd_reminder(message: Message, state: FSMContext):
    await message.answer("Что надо сделать?", reply_markup=reminder_keyboard())
    await state.set_state(ReminderState.reminderstate)


@reminder_router.message(ReminderState.reminderstate, lambda message: message.text == "Создать напоминание")
async def add_reminder(message: Message, state: FSMContext):
    await message.answer("Введи описание.")
    await state.set_state(ReminderState.createstate)


@reminder_router.message(ReminderState.createstate)
async def add_description_reminder(message: Message, state: FSMContext):
    rmndr = Reminder()
    rmndr.create_reminder(id_user=str(message.chat.id), description=message.text)
    await message.answer(text="Напоминание создано.")
    await state.set_state(ReminderState.reminderstate)

@reminder_router.message(ReminderState.reminderstate, lambda message: message.text == "Показать напоминания")
async def show_reminder(message: Message):
    rmndr = Reminder()
    user_reminder: dict = rmndr.show_reminder(str(message.chat.id))
    if len(user_reminder) != 0:
        text: str = ""
        for key, item in user_reminder.items():
            text += f"""
id напоминания: {item.get("id")}
Описание: {item.get("description")}
Время создания: {item.get("created_at")}
    """
        await message.answer(text=text)
    else:
        await message.answer(text="Нету напоминаний.")


@reminder_router.message(ReminderState.reminderstate, lambda message: message.text == "Удалить напоминание")
async def delete_reminder(message: Message, state: FSMContext):
    await message.answer(text="Введите id напоминания")
    await state.set_state(ReminderState.deletestate)


@reminder_router.message(ReminderState.deletestate)
async def id_delete_reminder(message: Message, state: FSMContext):
    rmndr = Reminder()
    boolean: bool = rmndr.delete_reminders(message.text)
    if boolean:
        await message.answer(text=f"Удалено напоминание {message.text}")
        await state.set_state(ReminderState.reminderstate)
    else:
        await message.answer(text="Проверьте правильность id или такого напоминания нет.")
