import os
import re
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from db.session import get_db
from crud.admin import admin_crud

from dotenv import load_dotenv
load_dotenv()

BOT_LINK = str(os.getenv('BOT_LINK'))
admin_management = Router()

CHECK_TG_ACCOUNT = re.compile(r'^@')


class TeamLeadName(StatesGroup):
    team_lead_username = State()


class RemoveTeamLead(StatesGroup):
    team_lead_username = State()


# Saving team_lead username to database for giving access to registration
@admin_management.message(TeamLeadName.team_lead_username)
async def adding_team_lead_username(message: Message, state: FSMContext):
    team_lead_username = message.text
    if CHECK_TG_ACCOUNT.match(team_lead_username):
        await state.update_data(team_lead_username=team_lead_username)
        data = await state.get_data()
        with get_db() as db:
            admin_crud.create(db=db, obj_in={
                'personal_tg_nick': f'{data['team_lead_username']}'
            })
        await message.answer('Скиньте тим лиду ссылку в бот, \n'
                             'для прохождения адаптации')
        await message.answer(BOT_LINK)
        await state.clear()
    else:
        await message.answer('Вы забыли символ @ вначале 😉')


# Remove team lead from database
"""Question: Should we remove team lead from database or just set dismissal date"""


@admin_management.message(RemoveTeamLead.team_lead_username)
async def fire_team_lead(message: Message, state: FSMContext):
    username = message.text
    if CHECK_TG_ACCOUNT.match(username):
        await state.update_data(username=username)
        data = await state.get_data()
        with get_db() as db:
            user = admin_crud.get_field_by_username(db=db, username=data['username'], field='id')
            admin_crud.remove(db=db, id=user)
            await message.answer('Тим лид удален из базы')
            await state.clear()
    else:
        await message.answer('Вы забыли символ @ вначале 😉')


# Show list of all team leads
async def team_lead_list(message: Message):
    with get_db() as db:
        admins = admin_crud.get_multi(db=db)
        admin_list = [f'{i}. {str(admin.personal_tg_nick)}, {str(admin.full_name)}, {admin.email}'
                      for i, admin in enumerate(admins, 1)]
        await message.answer('Вот Ваш список тим лидов: \n' + '\n'.join(admin_list))
