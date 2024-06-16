import os
import logging
import re
from datetime import datetime
from dotenv import load_dotenv

import asyncio

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from db.session import get_db, engine
from crud.user import user_crud
from models.user import Base

import keyboards as kb

from google_utilities.google_sheets import GoogleSheet
from google_utilities.google_drive import GoogleDriveLoad


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()
SUPERUSER = int(os.getenv('SUPERUSER'))


google_sheets_file_path = os.getenv('FILE_PATH')
google_sheet = GoogleSheet()

SHEETS_LIST = {
    'FFA_STUDENTS': os.getenv('FFA_STUDENTS'),
    'FFA_CRYPTO': os.getenv('FFA_CRYPTO')

}


team_leads_list = dict()
awaiting_team_lead_list = dict()

GROUP_CHATS_IDS = {
    'FIRST_GROUP_CHAT': int(os.getenv('FIRST_GROUP_CHAT')),
    'SECOND_GROUP_CHAT': int(os.getenv('SECOND_GROUP_CHAT')),
    'THIRD_GROUP_CHAT': int(os.getenv('THIRD_GROUP_CHAT'))
}

google_drive = GoogleDriveLoad()


class RegForm(StatesGroup):
    full_name = State()
    place = State()
    phone = State()
    birth = State()
    mail = State()
    discord = State()
    address = State()
    bank = State()
    selfie = State()


class Form(StatesGroup):
    name = State()


CHECK_FULL_NAME = re.compile(r'^[А-ЯЁЄІЇҐ][а-яёєіїґ]+\s[А-ЯЁЄІЇҐ][а-яёєіїґ]+\s[А-ЯЁЄІЇҐ][а-яёєіїґ]+$')
CHECK_PHONE = re.compile(r'^(\+?\d{12}|\d{10})$')
CHECK_BIRTH = re.compile(r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d\d$')
CHECK_MAIL = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
CHECK_CARD = re.compile(r'^\d{16}$')
CHECK_TRC = re.compile(r'^T[a-zA-Z0-9]{33}$')


def parse_date(date):
    date_form = datetime.strptime(date, '%d.%m.%Y')
    return date_form.strftime('%Y-%m-%d')


@dp.message(CommandStart())
async def welcome_message(message: Message):
    user = message.from_user.username
    with get_db() as db:
        await message.answer('Временная информация! \n'
                             '/admin - Админпанель, необходимо в env указать свой чат id \n'
                             '/team - Пишет пользователь, после админ должен подтвердить через "Добавить тим лида"')
        username = user_crud.get_user_by_username(db=db, username=user)
        if not username and user != SUPERUSER:
            await message.answer(f'Привет {message.from_user.first_name}, начнем регистрацию?',
                                 reply_markup=kb.registation)
        else:
            await message.answer('Вы уже зарегистрированы!')


@dp.callback_query(F.data == 'registration')
async def start_reg(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RegForm.full_name)
    await callback.message.answer('Введите Ваше ФИО')
    await callback.answer()


@dp.message(RegForm.full_name)
async def reg_name(message: Message, state: FSMContext):
    full_name = message.text
    if CHECK_FULL_NAME.fullmatch(full_name):
        await state.update_data(full_name=full_name)
        await state.set_state(RegForm.place)
        await message.answer('Введите город и страну проживания?')
    else:
        await message.answer('ФИО введено не верно! Введите в формате - Фимилия Имя Отчество')


@dp.message(RegForm.place)
async def reg_place(message: Message, state: FSMContext):
    await state.update_data(place=message.text)
    await state.set_state(RegForm.phone)
    await message.answer('Введите Ваш номер телефона')


@dp.message(RegForm.phone)
async def reg_phone(message: Message, state: FSMContext):
    phone = message.text
    if CHECK_PHONE.fullmatch(phone):
        await state.update_data(phone=phone)
        await state.set_state(RegForm.birth)
        await message.answer('Введите дату рождения в формате - ДД.ММ.ГГГГ')
    else:
        await message.answer('Введите номер телефона в формате +38050... или 050...')


@dp.message(RegForm.birth)
async def reg_birth(message: Message, state: FSMContext):
    birth = message.text
    if CHECK_BIRTH.fullmatch(birth):
        await state.update_data(birth=birth)
        await state.set_state(RegForm.mail)
        await message.answer('Введите Вашу почту')
    else:
        await message.answer('Некорретно ведена дата. Введите дату рождения в формате - ДД.ММ.ГГГГ')


@dp.message(RegForm.mail)
async def reg_mail(message: Message, state: FSMContext):
    mail = message.text.lower()
    if CHECK_MAIL.fullmatch(mail):
        await state.update_data(mail=mail)
        await state.set_state(RegForm.discord)
        await message.answer('Введите никнейм в Discord')
    else:
        await message.answer('Некорректно ведена почта')


@dp.message(RegForm.discord)
async def reg_discord(message: Message, state: FSMContext):
    await state.update_data(discord=message.text)
    await state.set_state(RegForm.address)
    await message.answer('Введите Ваш адрес')


@dp.message(RegForm.address)
async def reg_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(RegForm.bank)
    await message.answer('Введите номер карты или адрес кошелька (TRC-20)')


@dp.message(RegForm.bank)
async def reg_bank(message: Message, state: FSMContext):
    bank = message.text.replace(' ', '')
    if CHECK_TRC.fullmatch(bank) or CHECK_CARD.fullmatch(bank):
        await state.update_data(bank=bank)
        await state.set_state(RegForm.selfie)
        await message.answer('Сделайте селфи')
    else:
        await message.answer('Некорректно веден номер карты, введите повторно')


@dp.message(RegForm.selfie)
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


@dp.callback_query(F.data == 'finish_registration')
async def reg_finish(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
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
    personal_tg_nick = callback.from_user.username
    with get_db() as db:
        try:
            new_user_data = {
                "full_name": data['full_name'],
                "city": data['place'],
                "country": "Ukraine",  # Убедитесь, что значение корректно
                "phone": data['phone'],
                "birth_date": data['birth'],
                "email": data['mail'],
                "discord_nick": data['discord'],
                "postal_address": data['address'],
                "adaptation_start_date": current_date,  # Убедитесь, что значение корректно
                "work_start_date": None,  # Убедитесь, что значение корректно
                "assigned_stream": None,  # Убедитесь, что значение корректно
                "dismissal_date": None,  # Убедитесь, что значение корректно
                "admin_id": None,  # Убедитесь, что значение корректно
                "work_tg_nick": None,  # Убедитесь, что значение корректно
                "personal_tg_nick": f'{personal_tg_nick}',  # Убедитесь, что значение корректно
                "photo": file_link  # Убедитесь, что значение корректно
            }
            user_crud.create(db=db, obj_in=new_user_data)
        except Exception as e:
            db.rollback()
            logging.info(f'Ошибка записи в базу - {e}')
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer('Вы успешно зарегистрированы!')
    await bot.send_message(chat_id=SUPERUSER, text='У Вас новая регистрация')
    await invite_to_group_chats(chat_id)
    await share_to_sheets(data['mail'], data['full_name'], chat_id)
    await state.clear()


@dp.callback_query(F.data == 'repeat')
async def reg_repeat(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Давайте начнем с начала!')
    await state.clear()
    await start_reg(callback, state)


async def invite_to_group_chats(chat_id: int):
    for key in GROUP_CHATS_IDS:
        chats = GROUP_CHATS_IDS[key]
        invite_link = await bot.create_chat_invite_link(chat_id=chats)
        await bot.send_message(chat_id, invite_link.invite_link)
    await curators_instruction(chat_id)


async def curators_instruction(chat_id: int):
    await bot.send_message(chat_id, "Тут ти зможеш познайомитись більш детально з обов'язками які на тебе очікують "
                                    "\n❗ Перше з чого потрібно почати це гілка - Адаптація кураторів❗"
                                    "\nТакож я тримай посилання на 'Регламент роботи кураторів'",
                                    reply_markup=kb.notion_btn)


async def share_to_sheets(mail, full_name, chat_id):
    for key in SHEETS_LIST:
        sheet = SHEETS_LIST[key]
        google_sheet.share_sheet(sheet, mail)
    await bot.send_message(chat_id, text='Доступы к Google таблицам отправиленны на почту')
    google_sheet.copy_curator_template(mail, full_name)


@dp.message(Command('admin'))
async def admin_panel(message: Message):
    if message.from_user.id == SUPERUSER:
        await message.answer('Привет Админ!', reply_markup=kb.admin_main)
    else:
        await message.answer('Вы не Админ!')


@dp.message(Command('team'))
async def team_lead(message: Message):
    awaiting_team_lead_list[f'{message.from_user.id}'] = message.from_user.username
    print(awaiting_team_lead_list)
    await message.answer('Ожидайте подтверждения админа!')
    await bot.send_message(chat_id=SUPERUSER, text='У вас ожидает добавления тим лид!')


@dp.message(lambda message: message.text in ['Добавить Тим Лида', 'Уволить Тим Лида', 'Список Тим Лидов'])
async def reply_btn_admin(message: Message, state: FSMContext):
    if message.text == 'Добавить Тим Лида':
        await message.answer('Давайте добавим Тим Лида, открываю список ожидающих добавления')
        await awaiting_team_lead(message, state)
    elif message.text == 'Уволить Тим Лида':
        await message.answer('Давайте уволим Тим Лида, введите его ник в формате - @example')
    elif message.text == 'Список Тим Лидов':
        await message.answer('Готовлю список')


async def awaiting_team_lead(message: Message, state: FSMContext):
    for value in awaiting_team_lead_list.values():
        await message.answer(value)
    await message.answer('Кого добавим?')
    await state.set_state(Form.name)


@dp.message(Form.name)
async def adding_team_lead(message: Message, state: FSMContext):
    username = message.text
    if username in awaiting_team_lead_list.values():
        for key, value in awaiting_team_lead_list.items():
            if value == username:
                team_leads_list[key] = value
        key_to_delete = [key for key in team_leads_list if key in awaiting_team_lead_list]
        for key in key_to_delete:
            await bot.send_message(chat_id=key, text='Вы добалены в тим лиды')
            del awaiting_team_lead_list[key]
        await state.clear()
        await message.answer('Тим лид добавлен')
        print(awaiting_team_lead_list)
        print(team_leads_list)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
