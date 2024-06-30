import os
from datetime import datetime

from dotenv import load_dotenv

from aiogram import Bot, types, Router
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from db.session import get_db
from crud.user import user_crud

from helpers import (CHECK_FULL_NAME, CHECK_PHONE, CHECK_DATE, CHECK_MAIL, CHECK_TRC, CHECK_CARD, CHECK_TG_ACCOUNT,
                     parse_date)
import keyboards as kb

from google_utilities.google_drive import google_drive
from google_utilities.google_sheets import google_sheet

mentor_management = Router()

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)

SUPERUSER = int(os.getenv('SUPERUSER'))

# Goolgle sheets for sharing def share_to_sheets()
SHEETS_LIST = {
    'FFA_STUDENTS': os.getenv('FFA_STUDENTS'),
    'FFA_CRYPTO': os.getenv('FFA_CRYPTO')

}


team_leads_list = dict()
awaiting_team_lead_list = dict()


# Group chats for def invite_to_group_chats()
GROUP_CHATS_IDS = {
    'FIRST_GROUP_CHAT': int(os.getenv('FIRST_GROUP_CHAT')),
    'SECOND_GROUP_CHAT': int(os.getenv('SECOND_GROUP_CHAT')),
    'THIRD_GROUP_CHAT': int(os.getenv('THIRD_GROUP_CHAT'))
}


# State for registration mentor
class RegForm(StatesGroup):
    full_name = State()
    place = State()
    address = State()
    phone = State()
    birth = State()
    mail = State()
    discord = State()
    bank = State()
    selfie = State()


class Form(StatesGroup):
    name = State()


# State for saving mentor working telegram account
class TgForm(StatesGroup):
    tg_name = State()


# Starting function of mentor adaptation, set state
async def start_reg(message: Message, state: FSMContext):
    await state.set_state(RegForm.full_name)
    await message.answer('Введите Ваше ФИО')


# Save full name, change state
@mentor_management.message(RegForm.full_name)
async def reg_name(message: Message, state: FSMContext):
    full_name = message.text
    if CHECK_FULL_NAME.fullmatch(full_name):
        await state.update_data(full_name=full_name)
        await state.set_state(RegForm.place)
        await message.answer('Введите город и страну проживания?')
    else:
        await message.answer('ФИО введено не верно! Введите в формате - Фимилия Имя Отчество')


# Save city and country, change state
@mentor_management.message(RegForm.place)
async def reg_place(message: Message, state: FSMContext):
    await state.update_data(place=message.text)
    await state.set_state(RegForm.phone)
    await message.answer('Введите Ваш номер телефона')


# Save phone number, change state
@mentor_management.message(RegForm.phone)
async def reg_phone(message: Message, state: FSMContext):
    phone = message.text
    if CHECK_PHONE.fullmatch(phone):
        await state.update_data(phone=phone)
        await state.set_state(RegForm.birth)
        await message.answer('Введите дату рождения в формате - ДД.ММ.ГГГГ')
    else:
        await message.answer('Введите номер телефона в формате +38050... или 050...')


# Save birthdate, change state
@mentor_management.message(RegForm.birth)
async def reg_birth(message: Message, state: FSMContext):
    birth = message.text
    if CHECK_DATE.fullmatch(birth):
        await state.update_data(birth=birth)
        await state.set_state(RegForm.mail)
        await message.answer('Введите Вашу почту')
    else:
        await message.answer('Некорретно ведена дата. Введите дату рождения в формате - ДД.ММ.ГГГГ')


# Save email, change state
@mentor_management.message(RegForm.mail)
async def reg_mail(message: Message, state: FSMContext):
    mail = message.text.lower()
    if CHECK_MAIL.fullmatch(mail):
        await state.update_data(mail=mail)
        await state.set_state(RegForm.discord)
        await message.answer('Введите никнейм в Discord')
    else:
        await message.answer('Некорректно ведена почта')


# Save disord name, change state
@mentor_management.message(RegForm.discord)
async def reg_discord(message: Message, state: FSMContext):
    await state.update_data(discord=message.text)
    await state.set_state(RegForm.address)
    await message.answer('Введите Ваш адрес')


# Save full address, change state
@mentor_management.message(RegForm.address)
async def reg_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(RegForm.bank)
    await message.answer('Введите номер карты или адрес кошелька (TRC-20)')


# Save bank card number or usdt (TRC-20) wallet address, change state
@mentor_management.message(RegForm.bank)
async def reg_bank(message: Message, state: FSMContext):
    bank = message.text.replace(' ', '')
    if CHECK_TRC.fullmatch(bank) or CHECK_CARD.fullmatch(bank):
        await state.update_data(bank=bank)
        await state.set_state(RegForm.selfie)
        await message.answer('Сделайте селфи')
    else:
        await message.answer('Некорректно веден номер карты, введите повторно')


# Save photo-selfie, function provide confirm or decline input information
@mentor_management.message(RegForm.selfie)
async def reg_selfie(message: Message, state: FSMContext):
    if message.content_type == types.ContentType.PHOTO:
        photo_id = message.photo[-1].file_id
        await state.update_data(selfie=photo_id)
        data = await state.get_data()
        await message.answer(f'Проверьте Ваши данные: '
                             f'\n{data['full_name']} '
                             f'\n{data['place']} '
                             f'\n{data['phone']} '
                             f'\n{data['birth']} '
                             f'\n{data['mail']} '
                             f'\n{data['discord']} '
                             f'\n{data['address']} '
                             f'\n{data['bank']}')
        await bot.send_photo(chat_id=message.chat.id, photo=data['selfie'], reply_markup=kb.finish_registration)
    else:
        await message.answer('Сделайте селфи')


# Getting information from state + getting photo link from Google Drive and upload to the database,
# clearing class RegForm state
async def reg_finish(message: Message, state: FSMContext):
    await message.edit_reply_markup(reply_markup=None)
    chat_id = message.chat.id
    username = f'@{message.chat.username}'
    data = await state.get_data()
    file = await bot.get_file(data['selfie'])
    file_path = file.file_path
    local_photo = 'photo.jpg'
    await bot.download_file(file_path, local_photo)
    file_name = data['full_name'].replace(' ', '_')
    file_link = google_drive.download_photo(file_name, local_photo)
    os.remove(local_photo)
    data['birth'] = parse_date(data['birth'])
    current_date = datetime.now().strftime('%Y-%m-%d')
    with get_db() as db:
        find_user = user_crud.get_user_by_username(db=db, username=username)
        try:
            new_user_data = {
                'chat_id': chat_id,
                "full_name": data['full_name'],
                "city": data['place'],
                "phone": data['phone'],
                "birth_date": data['birth'],
                "email": data['mail'],
                "discord_nick": data['discord'],
                "postal_address": data['address'],
                "adaptation_start_date": current_date,
                "bank": data['bank'],
                "photo": file_link
            }
            user_crud.update(db=db, db_obj=find_user, obj_in=new_user_data)
        except Exception as e:
            db.rollback()
            print(f'Ошибка записи в базу - {e}')
    await message.answer('Вы успешно зарегистрированы!')
    await bot.send_message(chat_id=SUPERUSER, text='У Вас новая регистрация')
    await invite_to_group_chats(chat_id)
    await share_to_sheets(data['mail'], data['full_name'], chat_id)
    await state.clear()


# Function sending invatation link to the working telegram groups
async def invite_to_group_chats(chat_id: int):
    await bot.send_message(chat_id, text='👇Вам необходимо присоединится к следующим рабочим группам 👇')
    for key in GROUP_CHATS_IDS:
        chats = GROUP_CHATS_IDS[key]
        invite_link = await bot.create_chat_invite_link(chat_id=chats)
        await bot.send_message(chat_id, invite_link.invite_link)


# Funtion sharing Google Sheet worksheet
async def share_to_sheets(mail, full_name, chat_id):
    for key in SHEETS_LIST:
        sheet = SHEETS_LIST[key]
        google_sheet.share_sheet(sheet, mail)
    await bot.send_message(chat_id, text='Доступы к Google таблицам отправиленны на почту', reply_markup=kb.mentor_menu)
    google_sheet.copy_curator_template(mail, full_name)


# Function adding mentor`s working telegram account to the database and clearing class TgForm state
@mentor_management.message(TgForm.tg_name)
async def add_working_tg_number(message: Message, state: FSMContext):
    working_tg = message.text
    if CHECK_TG_ACCOUNT.match(working_tg):
        await state.update_data(tg_name=message.text)
        data = await state.get_data()
        user = f'@{message.from_user.username}'
        with get_db() as db:
            find_user = user_crud.get_user_by_username(db=db, username=user)
            user_crud.update(db=db, db_obj=find_user, obj_in={
                'work_tg_nick': data['tg_name']
            })
        await message.answer('Рабочий ТГ номер добавлен', reply_markup=kb.mentor_menu_full_registered)
        await state.clear()
    else:
        await message.answer('Вы забыли символ @ вначале 😉')
