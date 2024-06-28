from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню для выбора роли
role_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Админ', callback_data='role_admin')],
    [InlineKeyboardButton(text='Тим лид', callback_data='role_team_lead')],
    [InlineKeyboardButton(text='Наставник', callback_data='role_mentor')]
])

# Подменю для Админа
admin_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить Тим Лида', callback_data='admin_add_team_lead')],
    # Тут в принципе можем сделать так же как и добавления кураторов, только меньше полей,
    # можешь их посмотреть в модели админа.
    [InlineKeyboardButton(text='Уволить Тим Лида', callback_data='admin_remove_team_lead')],
    [InlineKeyboardButton(text='Список Тим Лидов', callback_data='admin_list_team_leads')],
    # возвращает с базы список ТЛдов инфы достаточно ТГ акк, ФИО, почта.
    [InlineKeyboardButton(text='Назад', callback_data='back_to_roles')]
])

# Подменю для Тим Лида
team_lead_menu_non_registered = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пройти адаптацию на тим лида', callback_data='team_lead_adaptation')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_roles')]
])


team_lead_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить наставника', callback_data='team_lead_add')],
    # после нажатия кнопки, надо вписать тг ник куратора (@example) которого хочешь доабвить и
    # ему автоматически летит приглос в бот, так же тут можно реализовать что бы сразу утсанавливало связь с ТЛдом
    # например записывало в данные ИД ТЛа и потмо когда сохраняешь в БД указывать форин кей с этим ТЛом
    [InlineKeyboardButton(text='Посмотреть свой список наставников', callback_data='team_lead_mine_list')],
    # Возвращает список всех наставников связанных с этим ТЛом (фильтрация оп айдишнику ТЛа), достаточно возвращить
    # ФИО, Рабочий ТГ ник, закрепленные потоки
    [InlineKeyboardButton(text='Посмотреть общий список наставников', callback_data='team_lead_general_list')],
    # Возвращает список всех наставников с БД
    [InlineKeyboardButton(text='Посмотреть информацию о конуретном наставнике', callback_data='team_lead_current_mentor')],
    # Ввобдит ТГ ник личный или рабочий выводится инфа про наставника,
    # Открывается меню с кнопками
    # "Назначить поток для наставника"
    # "Установить дату начала работы"
    # "Уволить наставника"
    [InlineKeyboardButton(text='Отправить сообщение для всех', callback_data='team_lead_message')],
    # Возможность запостить в бот какую то инфу для всех. Написать сообщение и что бы оно пришло всем кто есть в боте.
    # Не обязательно делать эту функцию
    [InlineKeyboardButton(text='Назад', callback_data='back_to_roles')]
])
team_lead_mentor_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назначить поток для наставника', callback_data='team_lead_stream')],
    [InlineKeyboardButton(text='Установить дату начала работы', callback_data='team_lead_start_date')],
    [InlineKeyboardButton(text='Уволить наставника', callback_data='team_lead_end_date')],
    [InlineKeyboardButton(text='Назад', callback_data='team_lead_clear')]
])
finish_team_lead_registration = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтвердить', callback_data='finish_team_lead_registration')],
    [InlineKeyboardButton(text='Пройти заново', callback_data='repeat_team_lead_registration')]
])


# Подменю для Наставника
mentor_menu_non_registred = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начать адаптацию', callback_data='mentor_adaptation_registration')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_roles')]
])
mentor_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Обязательно к прочтению', callback_data='mentor_read')],
    # Тут просто инфа возвращается я текст подготовлю
    [InlineKeyboardButton(text='Добавить рабочий аккаунт', callback_data='mentor_work')],
    [InlineKeyboardButton(text='Инструкция по созданию визитки и кружочка', callback_data='mentor_instruction')],
    # Тут просто инфа возвращается я текст подготовлю
    [InlineKeyboardButton(text='Получить рабочий аккаунт', callback_data='mentor_request')],
    # Тут летит сообщение с инструкцией как его получить. Тоже напишу.
    [InlineKeyboardButton(text='Назад', callback_data='back_to_roles')]
])
mentor_menu_full_registered = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Обязательно к прочтению', callback_data='mentor_read')],
    [InlineKeyboardButton(text='Инструкция по созданию визитки и кружочка', callback_data='mentor_instruction')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_mentor_menu')]
])
finish_registration = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтвердить', callback_data='finish_registration')],
    [InlineKeyboardButton(text='Пройти заново', callback_data='repeat_mentor_registration')]
])
notion_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👉Регламент роботи кураторів👈',
                          url='https://pollen-coneflower-6fa.notion.site/c7eee26c6e3344aa8d6c9fadd1b3dd68?pvs=4')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_mentor_menu')]
])
back_mentor_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_to_mentor_menu')]
])
