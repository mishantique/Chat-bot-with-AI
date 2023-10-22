from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Bot

import datetime

from data.states import User, ExistUser, Neworderauto
from data.states import Mycallback

from data.databases import db_table_val, conn, cursor

from config_reader import config

from keyboards import reply, fabrics

router = Router()
bot = Bot(config.bot_token.get_secret_value())
# Предполагается, что у тебя уже есть объект `cursor` и `conn` для работы с базой данных

@router.callback_query(Mycallback.filter(F.action == 'история заявок'))
async def start_order(call: CallbackQuery, callback_data: Mycallback):
    chat_id = call.message.chat.id
    user_name = call.from_user.first_name
    user_id = call.from_user.id

    # Получение всех заявок по user_id из базы данных
    cursor.execute('SELECT user_id, time, status FROM orders WHERE user_id = ?', (user_id,))
    results = cursor.fetchall()

    if results:
        # Если есть заявки, формируем сообщение
        message_text = f'Заявки пользователя {user_name}:\n'
        for user_id_db, time, status in results:
            message_text += f'Заявка от {time}\n'
    else:
        message_text = 'Активных заявок нет.'

    await bot.send_message(chat_id, message_text, reply_markup=fabrics.orders)