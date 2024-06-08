import os
import logging
import re
from dotenv import load_dotenv

import asyncio

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import keyboards as kb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()
SUPERUSER = int(os.getenv('SUPERUSER'))
curators_list = set()
GROUP_CHATS_IDS = {
    'FIRST_GROUP_CHAT': int(os.getenv('FIRST_GROUP_CHAT')),
    'SECOND_GROUP_CHAT': int(os.getenv('SECOND_GROUP_CHAT')),
    'THIRD_GROUP_CHAT': int(os.getenv('THIRD_GROUP_CHAT'))
}


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


CHECK_FULL_NAME = re.compile(r'^[А-ЯЁЄІЇҐ][а-яёєіїґ]+\s[А-ЯЁЄІЇҐ][а-яёєіїґ]+\s[А-ЯЁЄІЇҐ][а-яёєіїґ]+$')
CHECK_PHONE = re.compile(r'^(\+?\d{12}|\d{10})$')
CHECK_BIRTH = re.compile(r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d\d$')
CHECK_MAIL = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
CHECK_CARD = re.compile(r'^\d{16}$')
CHECK_TRC = re.compile(r'^T[a-zA-Z0-9]{33}$')


@dp.message(CommandStart())
async def welcome_message(message: Message):
    user = message.from_user.id
    if user not in curators_list and user != SUPERUSER:
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


@dp.message(RegForm.selfie)
async def reg_selfie(message: Message, state: FSMContext):
    if message.content_type == types.ContentType.PHOTO:
        photo = message.photo[-1].file_id
        await state.update_data(selfie=photo)
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
    curators_list.add(callback.message.chat.id)
    # data = await state.get_data()
    # Реализовать запись в Google Sheets
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer('Вы успешно зарегистрированы!')
    await state.clear()
    await bot.send_message(chat_id=SUPERUSER, text='У Вас новая регистрация')
    await invite_to_group_chats(chat_id)


"""Example how to use dependency with DB and save user in DB"""
#
#
# from sqlalchemy.orm import Session
# from dependencies import get_db_dependency
# from crud import user_crud
#
#
# # Другие импорты и настройки бота...
#
# @dp.callback_query(F.data == 'finish_registration')
# async def reg_finish(callback: CallbackQuery, state: FSMContext, db: Session = Depends(get_db_dependency)):
#     curators_list.add(callback.message.chat.id)
#
#     data = await state.get_data()
#
#     new_user_data = {
#         "full_name": data['full_name'],
#         "city": data['place'],
#         "country": "Ukraine",  # Убедитесь, что значение корректно
#         "phone": data['phone'],
#         "birth_date": data['birth'],
#         "email": data['mail'],
#         "discord_nick": data['discord'],
#         "postal_address": data['address'],
#         "adaptation_start_date": "2024-01-01",  # Убедитесь, что значение корректно
#         "work_start_date": None,  # Убедитесь, что значение корректно
#         "assigned_stream": None,  # Убедитесь, что значение корректно
#         "dismissal_date": None,  # Убедитесь, что значение корректно
#         "admin_id": None,  # Убедитесь, что значение корректно
#         "work_tg_nick": "work_tg_nick",  # Убедитесь, что значение корректно
#         "personal_tg_nick": "personal_tg_nick",  # Убедитесь, что значение корректно
#         "photo": "path/to/photo.jpg"  # Убедитесь, что значение корректно
#     }
#
#     new_user = user_crud.create(db=db, obj_in=new_user_data)
#     print(f"Created user: {new_user}")
#
#     await callback.message.edit_reply_markup(reply_markup=None)
#     await callback.message.answer('Вы успешно зарегистрированы!')
#     await state.clear()
#     await bot.send_message(chat_id=SUPERUSER, text='У Вас новая регистрация')


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


@dp.message(Command('admin'))
async def admin_panel(message: Message):
    if message.from_user.id == SUPERUSER:
        await message.answer('Привет Админ!', reply_markup=kb.admin_main)
    else:
        await message.answer('Вы не Админ!')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
