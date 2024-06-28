from aiogram import Router

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from telegram_bot.team_lead_management import (my_mentors, all_team_leads_mentors, TeamLeadForm,
                                               MentorName, CurrentMentor, SendMessage)
import telegram_bot.keyboards as kb

team_lead = Router()


@team_lead.callback_query(lambda callback: callback.data and callback.data.startswith('team_lead_'))
async def team_lead_menu_handler(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split('_')[2]
    if action == 'adaptation':
        await callback.message.answer('Ок...Давайте пройдем адаптицию \n'
                                      'Введите Ваше - ФИО')
        await state.set_state(TeamLeadForm.full_name)

    elif action == 'add':
        await callback.message.answer('Давайте добавим ментора, введите его ТГ имя - @username')
        await state.set_state(MentorName.mentor_username)

    elif action == 'mine':
        await my_mentors(callback.message)

    elif action == 'general':
        await all_team_leads_mentors(callback.message)

    elif action == 'current':
        await callback.message.answer('Введите ментора в формате - @example')
        await state.set_state(CurrentMentor.current_mentor)

    elif action == 'message':
        await callback.message.answer('Напишите что хотите отправить: ')
        await state.set_state(SendMessage.message)

    elif action == 'stream':
        await callback.message.answer('Введите номер потока:')
        await state.set_state(CurrentMentor.stream)

    elif action == 'start':
        await callback.message.answer('Введите дату начала работы ментора в формате - DD.MM.YYYY:')
        await state.set_state(CurrentMentor.start_date)

    elif action == 'end':
        await callback.message.answer('Введите дату увольнения ментора в формате - DD.MM.YYYY:')
        await state.set_state(CurrentMentor.end_date)

    elif action == 'clear':
        await state.clear()
        await callback.message.edit_text('Вы выбрали роль Тим лид. Вот ваше меню:', reply_markup=kb.team_lead_menu)


        