import os
from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
load_dotenv()
from db.session import get_db
from crud.user import user_crud
from crud.admin import admin_crud

from telegram_bot.admin_management import TeamLeadName, RemoveTeamLead, team_lead_list


admin_handler = Router()


@admin_handler.callback_query(lambda callback: callback.data and callback.data.startswith('admin_'))
async def admin_handler_menu_handler(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split('_')[1]
    if action == 'add':
        await callback.message.answer('Добавляем Тим Лида...Введите пользователя в формате @example')
        await state.set_state(TeamLeadName.team_lead_username)
    elif action == 'remove':
        await callback.message.answer('Введите пользователя в формате @example')
        await state.set_state(RemoveTeamLead.team_lead_username)
    elif action == 'list':
        await team_lead_list(callback.message)
