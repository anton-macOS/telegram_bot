from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

admin_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Список админов'), KeyboardButton(text='Удалить админа')]
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
