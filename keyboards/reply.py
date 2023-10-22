from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

main = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = 'Клиент'),
            KeyboardButton(text = 'Администратор')
        ],
        [
            KeyboardButton(text = 'Информация'),
            KeyboardButton(text = 'Сотрудник')
        ]
    ],
    resize_keyboard = True,
    one_time_keyboard = True,
    input_field_placeholder = 'Выберите действие из меню',
    selective = True
)

main_admin = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = 'Новые заявки'),
        ],
        [
            KeyboardButton(text = 'История заявок клиентов')
        ]
    ],
    resize_keyboard = True,
    one_time_keyboard = True,
    input_field_placeholder = 'Выберите действие из меню',
    selective = True
)