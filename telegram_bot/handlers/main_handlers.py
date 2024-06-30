import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from telegram_bot.logger_setup import logger
load_dotenv()
SUPERUSER = int(os.getenv('SUPERUSER'))

from db.session import get_db
from crud.user import user_crud
from crud.admin import admin_crud

import telegram_bot.keyboards as kb

main_handler = Router()


@main_handler.message(CommandStart())
async def welcome_message(message: Message):
    await message.answer("Выберите роль:", reply_markup=kb.role_menu)


@main_handler.callback_query(lambda callback: callback.data and callback.data.startswith('role_'))
async def role_selection(callback: CallbackQuery):
    role = callback.data.split('_')[1]
    with get_db() as db:
        chat_id = callback.from_user.id
        user = f'@{callback.from_user.username}'
        if role == 'admin':
            if chat_id == SUPERUSER:
                await callback.message.edit_text("Вы выбрали роль Админ. Вот ваше меню:", reply_markup=kb.admin_menu)
        elif role == 'team':
            username = admin_crud.get_user_by_username(db=db, username=user)
            check_full_name = admin_crud.get_field_by_username(db=db, username=user, field='full_name')
            if username is None:
                await callback.message.answer('Вход запрещен, свяжитесь с Админом')
            elif check_full_name is None:
                await callback.message.edit_text('Вы не зарегистрированы, пройдите адаптацию тим лида:',
                                                 reply_markup=kb.team_lead_menu_non_registered)
            else:
                await callback.message.edit_text("Вы выбрали роль Тим лид. Вот ваше меню: ",
                                                 reply_markup=kb.team_lead_menu)
        elif role == 'mentor':
            username = user_crud.get_user_by_username(db=db, username=user)
            check_working_tg = user_crud.get_field_by_username(db=db, username=user, field='work_tg_nick')
            check_full_name = user_crud.get_field_by_username(db=db, username=user, field='full_name')
            if username is None:
                await callback.message.answer('Вход запрещен, свяжитесь с Тим Лидом')
            elif check_full_name is None:
                await callback.message.edit_text('Вы не зарегистрированы, пройдите адаптацию:',
                                                 reply_markup=kb.mentor_menu_non_registred)
            elif check_working_tg is None:
                await callback.message.edit_text('Вы выбрали роль Наставник. Вот ваше меню:',
                                                 reply_markup=kb.mentor_menu)
            else:
                await callback.message.edit_text('Вы выбрали роль Наставник. Вот ваше меню:',
                                                 reply_markup=kb.mentor_menu_full_registered)


@main_handler.callback_query(lambda callback: callback.data == 'back_to_roles')
async def back_to_roles(callback: CallbackQuery):
    await callback.message.edit_text("Выберите роль:", reply_markup=kb.role_menu)



