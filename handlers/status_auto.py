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
# Предполагается, что у тебя уже есть объект `cursor` и `conn` для работы с базой данных

@router.callback_query(Mycallback.filter(F.action == 'узнать статус'))
async def start_order(call: CallbackQuery, callback_data: Mycallback):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    user_name = call.from_user.first_name

    # Получение всех заявок по user_id из базы данных
    cursor.execute('SELECT user_id, time, status FROM orders WHERE user_id = ?', (user_id,))
    results = cursor.fetchall()

    if results:
        # Если есть заявки, формируем сообщение
        message_text = f'Заявки пользователя {user_name}:\n'
        for user_id_db, time, status in results:
            if status == 'rejected':
                # Если статус 'rejected', добавляем комментарий
                cursor.execute('SELECT commentary FROM orders WHERE time = ?', (time,))
                commentary_result = cursor.fetchone()
                commentary = commentary_result[0] if commentary_result else 'Отсутствует комментарий'
                message_text += f'К сожалению, заявка от {time} не соответствует установленным требованиям: \n' \
                                f'Пожалуйста, ознакомьтесь с комментарием о необходимых корректировках и отправьте заявку повторно: {commentary}'
            elif status == 'applied':
                # Если статус 'applied', добавляем соответствующее сообщение
                message_text += f'Заявка от {time} в состоянии "Одобрена". Для получения акта осмотра, пожалуйста, проверьте историю сообщений с ботом\n'
            else:
                message_text += f'Заявка от {time} в состоянии "На рассмотрении"\n'
    else:
        message_text = 'Активных заявок нет.'

    await bot.send_message(chat_id, message_text, reply_markup=fabrics.orders)