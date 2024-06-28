from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from db.session import get_db
from crud.user import user_crud

from telegram_bot.mentor_management import start_reg, reg_finish, TgForm
import telegram_bot.keyboards as kb
mentor_handler = Router()


@mentor_handler.callback_query(lambda callback: callback.data and callback.data.startswith('mentor_'))
async def mentor_handler_menu_handler(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split('_')[1]
    if action == 'adaptation':
        await callback.message.answer("Начинаем адаптацию")
        await start_reg(callback.message, state)
    elif action == 'read':
        await callback.message.edit_text("Тут ти зможеш познайомитись більш детально з обов'язками які на тебе"
                                         " очікують. \n ❗Перше з чого потрібно почати це гілка - Адаптація"
                                         " кураторів❗\n Також я тримай посилання на 'Регламент роботи кураторів'\n",
                                         reply_markup=kb.notion_btn)
    elif action == 'work':
        await state.set_state(TgForm.tg_name)
        await callback.message.answer('Введите рабочий ТГ аккаунт в формате - @example')
    elif action == 'instruction':
        await callback.message.answer('Инструкция по созданию визитки и кружочка: \n'
                                      '🤪 \n'
                                      '🤪 \n'
                                      '🤪 \n'
                                      '🤪 \n'
                                      '🤪 \n'
                                      'Вот так вот!', reply_markup=kb.back_mentor_menu)
    elif action == 'request':
        await callback.message.answer('Получить рабочий аккаунт: \n'
                                      'Чтобы получить рабочий аккаунт Вам нужно связаться с @Velentina \n'
                                      'Вот так вот!')


@mentor_handler.callback_query(lambda callback: callback.data == 'finish_registration')
async def finish_mentor_handler_registration(callback: CallbackQuery, state: FSMContext):
    await reg_finish(callback.message, state)


@mentor_handler.callback_query(lambda callback: callback.data == 'repeat_mentor_handler_registration')
async def repeat_mentor_handler_registration(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Давайте начнем с начала!')
    await state.clear()
    await start_reg(callback.message, state)


@mentor_handler.callback_query(lambda callback: callback.data == 'back_to_mentor_menu')
async def back_to_mentor_handler_menu(callback: CallbackQuery):
    with get_db() as db:
        user = f'@{callback.from_user.username}'
        check_working_tg = user_crud.get_field_by_username(db=db, username=user, field='work_tg_nick')
        if check_working_tg is None:
            await callback.message.edit_text('Вы выбрали роль Наставник. Вот ваше меню:',
                                             reply_markup=kb.mentor_menu)
        else:
            await callback.message.edit_text('Вы выбрали роль Наставник. Вот ваше меню:',
                                             reply_markup=kb.mentor_menu_full_registered)
