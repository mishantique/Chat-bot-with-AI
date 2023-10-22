from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.types import Message, CallbackQuery
from aiogram.filters.callback_data import CallbackData

from data.states import Mycallback

link = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = 'Официальный сайт', url = 'https://sovcombank.ru/')
        ]
    ]
)
