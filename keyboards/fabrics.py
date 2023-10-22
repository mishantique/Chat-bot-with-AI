from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from data.states import Mycallback
from data.databases import db_table_val, conn, cursor

auth_reg = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = 'Авторизация',
                                 callback_data = Mycallback(action = 'авторизация').pack()),
        ],
        [
            InlineKeyboardButton(text = 'Регистрация',
                                 callback_data = Mycallback(action = 'регистрация').pack()),
        ]
    ]
)


auth_reg_insurer = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = 'Авторизация',
                                 callback_data = Mycallback(action = 'авторизация сотрудник').pack()),
        ],
        [
            InlineKeyboardButton(text = 'Регистрация',
                                 callback_data = Mycallback(action = 'регистрация сотрудник').pack()),
        ]
    ]
)



auth = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = 'Авторизация',
                                 callback_data = Mycallback(action = 'авторизация').pack()),
        ],
    ]
)


auth_insurer = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = 'Авторизация',
                                 callback_data = Mycallback(action = 'авторизация сотрудник').pack()),
        ],
    ]
)

orders = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = 'Подать заявку',
                                 callback_data = Mycallback(action = 'подать заявку').pack()),
            InlineKeyboardButton(text = 'История заявок',
                                 callback_data = Mycallback(action = 'история заявок').pack()),
        ],
        [
            InlineKeyboardButton(text='Узнать статус заявки',
                                 callback_data=Mycallback(action='узнать статус').pack()),
        ]
    ]
)


orders_insurer = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = 'Новые заявки',
                                 callback_data = Mycallback(action = 'новые заявки страховщик').pack()),
        ],
        [
            InlineKeyboardButton(text = 'История обработки заявок',
                                 callback_data = Mycallback(action = 'история заявок страховщик').pack()),
        ]
    ]
)


# Получение уникальных значений времени из таблицы 'orders'
cursor.execute('SELECT DISTINCT time FROM orders WHERE status = "active"')
your_list_of_times = [row[0] for row in cursor.fetchall()]


def get_orders_list_insurer(your_list_of_times):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f'Заявка от {time} из orders',
                    callback_data=Mycallback(action = f'заявка_{index}').pack()
                ),
            ] for index, time in enumerate(your_list_of_times, start=1)
        ]
    )


def get_orders_list_admin(your_list_of_times):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f'Заявка от {time} из orders',
                    callback_data=Mycallback(action = f'админ заявка_{index}').pack()
                ),
            ] for index, time in enumerate(your_list_of_times, start=1)
        ]
    )

response_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Связаться с клиентом", callback_data=Mycallback(action="связаться").pack()),
            InlineKeyboardButton(text="Отклонить заявку", callback_data=Mycallback(action="отклонить").pack()),
            InlineKeyboardButton(text="Принять заявку", callback_data=Mycallback(action="принять").pack()),
        ]
    ]
)

response_keyboard1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отклонить заявку", callback_data=Mycallback(action="отклонить").pack()),
            InlineKeyboardButton(text="Принять заявку", callback_data=Mycallback(action="принять").pack()),
        ]
    ]
)

order_type = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = 'Автомобиль',
                                 callback_data = Mycallback(action = 'автомобиль').pack()),
            InlineKeyboardButton(text = 'Загородный дом',
                                 callback_data = Mycallback(action = 'загородный дом').pack())
        ],
    ]
)

opportunities_auto = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = 'Справка',
                                 callback_data = Mycallback(action = 'справка').pack()),
            InlineKeyboardButton(text='Загрузить фото',
                                 callback_data=Mycallback(action='загрузить фотографии').pack())
        ],
        [
            InlineKeyboardButton(text = 'Требования к фотоматериалам',
                                 callback_data = Mycallback(action = 'требования к фотоматериалам').pack())
        ],
        [
            InlineKeyboardButton(text = 'Добавить описание объекта',
                                 callback_data = Mycallback(action = 'добавить описание').pack())
        ]
    ]
)


opportunities_auto1 = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = 'Требования к фотоматериалам',
                                 callback_data = Mycallback(action = 'требования к фотоматериалам').pack())
        ],
        [
            InlineKeyboardButton(text = 'Загрузить фото',
                                 callback_data = Mycallback(action = 'загрузить фотографии').pack())
        ]
    ]
)


opportunities_auto2 = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = 'Справка',
                                 callback_data = Mycallback(action = 'справка').pack())
        ],
        [
            InlineKeyboardButton(text = 'Загрузить фото',
                                 callback_data = Mycallback(action = 'загрузить фотографии').pack())
        ]
    ]
)


damage_auto = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = 'Повреждения отсутствуют',
                                 callback_data = Mycallback(action = 'повреждения отсутствуют').pack())
        ],
        [
            InlineKeyboardButton(text = 'Повреждения есть',
                                 callback_data = Mycallback(action = 'повреждения есть').pack())
        ]
    ]
)

keys_auto = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = 'Есть в наличии',
                                 callback_data = Mycallback(action = 'ключи есть').pack())
        ],
        [
            InlineKeyboardButton(text = 'Отсутствуют',
                                 callback_data = Mycallback(action = 'ключей нет').pack())
        ]
    ]
)


opportunities_house = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = 'Справка',
                                 callback_data = Mycallback(action = 'справка дом').pack())
        ],
        [
            InlineKeyboardButton(text = 'Требования к фотоматериалам',
                                 callback_data = Mycallback(action = 'требования к фотоматериалам дом').pack())
        ],
        [
            InlineKeyboardButton(text = 'Загрузить фото',
                                 callback_data = Mycallback(action = 'загрузить фотографии дом').pack())
        ],
        [
            InlineKeyboardButton(text = 'Добавить описание объекта',
                                 callback_data = Mycallback(action = 'добавить описание дом').pack())
        ]
    ]
)


opportunities_house1 = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = 'Требования к фотоматериалам',
                                 callback_data = Mycallback(action = 'требования к фотоматериалам дом').pack())
        ],
        [
            InlineKeyboardButton(text = 'Загрузить фото',
                                 callback_data = Mycallback(action = 'загрузить фотографии дом').pack())
        ]
    ]
)


opportunities_house2 = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = 'Справка',
                                 callback_data = Mycallback(action = 'справка дом').pack())
        ],
        [
            InlineKeyboardButton(text = 'Загрузить фото',
                                 callback_data = Mycallback(action = 'загрузить фотографии дом').pack())
        ]
    ]
)


docs_house = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = 'документ есть',
                                 callback_data = Mycallback(action = 'документ есть').pack())
        ],
        [
            InlineKeyboardButton(text = 'документ отсутствует',
                                 callback_data = Mycallback(action = 'документа нет').pack())
        ]
    ]
)