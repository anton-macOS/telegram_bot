import os

from datetime import date
from aiogram import Router, Bot

from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from db.session import get_db
from crud.user import user_crud
from crud.admin import admin_crud
from logger_setup import logger
from telegram_bot.helpers import parse_date, CHECK_FULL_NAME, CHECK_MAIL, CHECK_TG_ACCOUNT, CHECK_DATE, find_admin_id
import telegram_bot.keyboards as kb

from dotenv import load_dotenv

load_dotenv()

team_lead_management = Router()

BOT_LINK = str(os.getenv('BOT_LINK'))


class TeamLeadForm(StatesGroup):
    full_name = State()
    email = State()
    work_start_date = State()


class MentorName(StatesGroup):
    mentor_username = State()


class CurrentMentor(StatesGroup):
    current_mentor = State()
    stream = State()
    start_date = State()
    end_date = State()


class SendMessage(StatesGroup):
    message = State()


# Registration team_lead, saving full name, changing state
@team_lead_management.message(TeamLeadForm.full_name)
async def team_lead_name(message: Message, state: FSMContext):
    full_name = message.text
    if CHECK_FULL_NAME.fullmatch(full_name):
        await state.update_data(full_name=full_name)
        await state.set_state(TeamLeadForm.email)
        await message.answer('Введите Вашу эл.почту:')
    else:
        await message.answer('ФИО введено не верно! Введите в формате - Фимилия Имя Отчество')


# Saving email, save to database and clearing state
@team_lead_management.message(TeamLeadForm.email)
async def team_lead_email(message: Message, state: FSMContext):
    find_user = f'@{message.chat.username}'
    chat_id = message.chat.id
    start_date = date.today()
    email = message.text.lower()
    if CHECK_MAIL.fullmatch(email):
        await state.update_data(email=email)
        data = await state.get_data()
        with get_db() as db:
            user = admin_crud.get_user_by_username(db=db, username=find_user)
            admin_crud.update(db=db, db_obj=user, obj_in={
                'chat_id': chat_id,
                'full_name': data['full_name'],
                'email': data['email'],
                'work_start_date': start_date
            })
            await message.answer('Спасибо, Вы прошли адаптацию!,', reply_markup=kb.team_lead_menu)
            await state.clear()
    else:
        await message.answer('Некорректно ведена почта')


# Adding mentor username to database for giving access for registration
@team_lead_management.message(MentorName.mentor_username)
async def add_new_mentor(message: Message, state: FSMContext):
    mentor_username = message.text
    admin_id = await find_admin_id(f'@{message.chat.username}')
    if CHECK_TG_ACCOUNT.match(mentor_username):
        await state.update_data(mentor_username=mentor_username)
        data = await state.get_data()
        with get_db() as db:
            user_crud.create(db=db, obj_in={
                'personal_tg_nick': data['mentor_username'],
                'admin_id': admin_id
            })
            await message.answer('Наставник добавлен, скиньте ему ссылку на бот и пусть начинает адаптацию')
            await message.answer(BOT_LINK)
            await state.clear()
    else:
        await message.answer('Вы забыли символ @ вначале 😉')


# Show current team lead`s mentor list
async def my_mentors(message: Message):
    with get_db() as db:
        username = f'@{message.chat.username}'
        admin_id = admin_crud.get_field_by_username(db=db, username=username, field='id')
        users = user_crud.get_users_by_admin_id(db=db, admin_id=admin_id)
        if not users:
            await message.answer('У вас пока нет наставников. Добавте наставника!')
        else:
            user_list = [(f'{i}. {str(user.full_name)}, {str(user.personal_tg_nick)}, '
                          f'{user.assigned_stream if user.assigned_stream is not None else 'поток не назначен'}')
                         for i, user in enumerate(users, 1)]
            await message.answer('Вот Ваш список наставников: \n' + '\n'.join(user_list))


# Show all list mentors with their team leads
async def all_team_leads_mentors(message: Message):
    with get_db() as db:
        admins = admin_crud.get_multi(db)
        for admin in admins:
            users = user_crud.get_users_by_admin_id(db=db, admin_id=admin.id)
            admin_info = f'<b>Тим лид: {admin.personal_tg_nick}</b>'
            user_list = [(f'{i}. {str(user.full_name)}, {str(user.personal_tg_nick)}, '
                          f'{user.assigned_stream if user.assigned_stream is not None else 'поток не назначен'}')
                         for i, user in enumerate(users, 1)]
            await message.answer(f'{admin_info} \n' + '\n'.join(user_list), parse_mode=ParseMode.HTML)


# Find information about current mentor
@team_lead_management.message(CurrentMentor.current_mentor)
async def find_current_mentor(message: Message, state: FSMContext, mentor_name: str = None):
    if mentor_name is None:
        mentor_name = message.text
    if CHECK_TG_ACCOUNT.match(mentor_name):
        await state.update_data(mentor_name=mentor_name)
        data = await state.get_data()
        mentor_data = data['mentor_name']
        with get_db() as db:
            mentor = user_crud.get_users_by_two_cols(db=db, username=mentor_data)
            if mentor is None:
                await message.answer('Наставник с таким имене не найден')
            else:
                await message.answer(f'Вот краткая информация о наставнике: \n'
                                     f'ФИО - {mentor.full_name} \n'
                                     f'Моб. - {mentor.phone} \n'
                                     f'Email - {mentor.email} \n'
                                     f'Поток - {
                                        mentor.assigned_stream 
                                        if mentor.assigned_stream is not None else 'поток не назначен'
                                     } \n'
                                     f'Дата начала работы - {
                                        mentor.work_start_date if
                                        mentor.work_start_date is not None else 'дата начала не назначена'
                                     } \n'
                                     f'Cтатус наставника - '
                                     f'{'Уволен' if mentor.dismissal_date is not None else 'Работает'}',
                                     reply_markup=kb.team_lead_mentor_menu)
    else:
        await message.answer('Вы забыли символ @ вначале 😉')


# Set assigned mentor stream to database
@team_lead_management.message(CurrentMentor.stream)
async def set_mentor_stream(message: Message, state: FSMContext):
    stream = message.text
    await state.update_data(stream=stream)
    data = await state.get_data()
    with get_db() as db:
        user = user_crud.get_user_by_username(db=db, username=data['mentor_name'])
        user_crud.update(db=db, db_obj=user, obj_in={
            'assigned_stream': stream
        })
        await message.answer('Поток записан')
        await find_current_mentor(message, state, mentor_name=data['mentor_name'])


# Set start working date of mentor
@team_lead_management.message(CurrentMentor.start_date)
async def set_mentor_start_date(message: Message, state: FSMContext):
    start_date = message.text
    if CHECK_DATE.fullmatch(start_date):
        await state.update_data(start_date=start_date)
        data = await state.get_data()
        with get_db() as db:
            user = user_crud.get_user_by_username(db=db, username=data['mentor_name'])
            user_crud.update(db=db, db_obj=user, obj_in={
                'work_start_date': parse_date(start_date)
            })
            await message.answer('Дата старта записана')
            await find_current_mentor(message, state, mentor_name=data['mentor_name'])
    else:
        await message.answer('Не верный формат, введите в формате - DD.MM.YYYY:')


# Set dismissal date of mentor
@team_lead_management.message(CurrentMentor.end_date)
async def fire_mentor(message: Message, state: FSMContext):
    end_date = message.text
    if CHECK_DATE.fullmatch(end_date):
        await state.update_data(start_date=end_date)
        data = await state.get_data()
        with get_db() as db:
            user = user_crud.get_user_by_username(db=db, username=data['mentor_name'])
            user_crud.update(db=db, db_obj=user, obj_in={
                'dismissal_date': parse_date(end_date)
            })
            await message.answer('Наставник уволен')
            await find_current_mentor(message, state, mentor_name=data['mentor_name'])
    else:
        await message.answer('Не верный формат, введите в формате - DD.MM.YYYY:')


# Send message to all team leads and mentors
@team_lead_management.message(SendMessage.message)
async def send_message_to_all(message: Message, state: FSMContext, bot: Bot):
    sender_chat_id = message.chat.id
    message = message.text
    await state.update_data(message=message)
    data = await state.get_data()
    send_message = data['message']
    with get_db() as db:
        users_chats = user_crud.get_all_chat_ids(db=db)
        admin_chats = admin_crud.get_all_chat_ids(db=db)
        all_chat_ids = users_chats + admin_chats
        for chat_id in all_chat_ids:
            if chat_id != sender_chat_id:
                try:
                    await bot.send_message(chat_id=chat_id, text=send_message)
                except Exception as e:
                    logger.info(f'Не удалось отправить сообщение - {chat_id}: {e}')
