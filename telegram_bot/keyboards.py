from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#
# # Главное меню для выбора роли
# role_menu = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Админ', callback_data='role_admin')],
#     [InlineKeyboardButton(text='Тим лид', callback_data='role_team_lead')],
#     [InlineKeyboardButton(text='Наставник', callback_data='role_mentor')]
# ])
#
# # Подменю для Админа
# admin_menu = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Добавить Тим Лида', callback_data='admin_add_team_lead')],
#     # Тут в принципе можем сделать так же как и добавления кураторов, только меньше полей,
#     # можешь их посмотреть в модели админа.
#     [InlineKeyboardButton(text='Уволить Тим Лида', callback_data='admin_remove_team_lead')],
#     [InlineKeyboardButton(text='Список Тим Лидов', callback_data='admin_list_team_leads')],
#     # возвращает с базы список ТЛдов инфы достаточно ТГ акк, ФИО, почта.
#     [InlineKeyboardButton(text='Назад', callback_data='back_to_roles')]
# ])
#
# # Подменю для Тим Лида
# team_lead_menu = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Добавить наставника', callback_data='team_lead_option1')],
#     # после нажатия кнопки, надо вписать тг ник куратора (@example) которого хочешь доабвить и
#     # ему автоматически летит приглос в бот, так же тут можно реализовать что бы сразу утсанавливало связь с ТЛдом
#     # например записывало в данные ИД ТЛа и потмо когда сохраняешь в БД указывать форин кей с этим ТЛом
#     [InlineKeyboardButton(text='Посмотреть свой список наставников', callback_data='team_lead_option2')],
#     # Возвращает список всех наставников связанных с этим ТЛом (фильтрация оп айдишнику ТЛа), достаточно возвращить
#     # ФИО, Рабочий ТГ ник, закрепленные потоки
#     [InlineKeyboardButton(text='Посмотреть общий список наставников', callback_data='team_lead_option3')],
#     # Возвращает список всех наставников с БД
#     [InlineKeyboardButton(text='Посмотреть информацию о конуретном наставнике', callback_data='team_lead_option4')],
#     # Ввобдит ТГ ник личный или рабочий выводится инфа про наставника,
#     # Открывается меню с кнопками
#     # "Назначить поток для наставника"
#     # "Установить дату начала работы"
#     # "Уволить наставника"
#
#     [InlineKeyboardButton(text='Отправить сообщение для всех', callback_data='team_lead_option5')],
#     # Возможность запостить в бот какую то инфу для всех. Написать сообщение и что бы оно пришло всем кто есть в боте.
#     # Не обязательно делать эту функцию
#
#
#     [InlineKeyboardButton(text='Назад', callback_data='back_to_roles')]
# ])
#
# # Подменю для Наставника
# mentor_menu = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Обязательно к прочтению', callback_data='mentor_option0')],
#     # Тут просто инфа возвращается я текст подготовлю
#     [InlineKeyboardButton(text='Начать адаптацию', callback_data='mentor_option1')],
#     # Тут происходит все что ты делал в регистрации
#     [InlineKeyboardButton(text='Добавить рабочий аккаунт', callback_data='mentor_option2')],
#     # Тут после выдачи ему рабочего аккаунта он нажмет кнопку Добавить рабочий аккаунт' и должен ввести ник в ТГ @example
#     # соответственно записыываем его в БД.
#     [InlineKeyboardButton(text='Инструкция по созданию визитки и кружочка', callback_data='mentor_option3')],
#     # Тут просто инфа возвращается я текст подготовлю
#     [InlineKeyboardButton(text='Получить рабочий аккаунт', callback_data='mentor_option3')],
#     # Тут летит сообщение с инструкцией как его получить. Тоже напишу.
#     [InlineKeyboardButton(text='Назад', callback_data='back_to_roles')]
# ])
#

admin_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить Тим Лида'), KeyboardButton(text='Уволить Тим Лида')],
    [KeyboardButton(text='Список Тим Лидов')]
], resize_keyboard=True)

registation = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Зарегистрироваться', callback_data='registration')]
])
finish_registration = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтвердить', callback_data='finish_registration')],
    [InlineKeyboardButton(text='Пройти заново', callback_data='repeat')]
])
notion_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👉Регламент роботи кураторів👈',
                          url='https://pollen-coneflower-6fa.notion.site/c7eee26c6e3344aa8d6c9fadd1b3dd68?pvs=4')]
])