from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Bot

import datetime

from data.states import User, ExistUser, Neworderauto, Order
from data.states import Mycallback

from data.databases import db_table_val, conn, cursor

from config_reader import config

from keyboards import reply, fabrics
from config_reader import config

from keyboards.fabrics import get_orders_list_insurer, get_orders_list_admin

from data.databases import db_table_val, conn, cursor, write_to_file, read_blob_data, read_doc_data

from handlers import orders_insurer

import base64
import io


router = Router()
bot = Bot(config.bot_token.get_secret_value())

@router.message(F.text =='История заявок клиентов')
async def answer(message: Message):
    msg = message.text.lower()

    chat_id = message.from_user.id
    user_name = message.from_user.first_name

    if msg == 'история заявок клиентов':
        await message.answer('Вот активные заявки:', reply_markup=reply.main_admin)

        # Получение всех заявок из базы данных
        cursor.execute('SELECT user_id, time, status FROM orders')
        results = cursor.fetchall()

        if results:
            # Если есть заявки, формируем сообщение
            message_text = f'История заявок:\n'
            for user_id_db, time, status in results:
                message_text += f"Заявка {user_id_db} из orders, взятая в рассмотрение {time} из orders, находится в статусе {status} из orders\n"
        else:
            message_text = 'Активных заявок нет.'

        await bot.send_message(chat_id, message_text, reply_markup=reply.main_admin)


@router.message(F.text =='Новые заявки')
async def start_order(message: Message, state: FSMContext):
    print("Обработчик для новых заявок администратора сработал!")
    chat_id = message.chat.id

    # Получение всех уникальных времен из базы данных
    cursor.execute('SELECT DISTINCT time FROM orders WHERE status = ?', ('active',))
    your_list_of_times = [row[0] for row in cursor.fetchall()]

    if your_list_of_times:
        # Если есть времена, формируем сообщение
        message_text = f'На рассмотрение предлагаются следующие заявки:\n'
        for index, time in enumerate(your_list_of_times, start=1):
            message_text += f'Заявка от {time}\n'

        # Создаем клавиатуру с обновленным your_list_of_times
        orders_list_insurer = get_orders_list_admin(your_list_of_times)
    else:
        message_text = 'Активных заказов нет.'
        orders_list_insurer = get_orders_list_insurer([])  # Пустой список времен
    await bot.send_message(
        chat_id=str(chat_id),
        text=str(message_text),
        reply_markup=orders_list_insurer
    )


@router.message(F.text =='История заявок')
async def start_order(message: Message, state: FSMContext):
    chat_id = message.chat.id

    # Получение всех заказов из базы данных
    cursor.execute('SELECT orders.time, orders.status, users.name, users.surname '
                   'FROM orders '
                   'JOIN users ON orders.user_id = users.user_id')
    results = cursor.fetchall()

    if results:
        # Если есть заказы, формируем сообщение
        message_text = f'В базе данных присутствует информация о следующих заявках:\n'
        for row in results:
            # row - это кортеж, используйте индексы для доступа к значениям
            message_text += f'Заявка от {row[0]} сформирована {row[2]} {row[3]}. Находится в состоянии {row[1]}\n'
    else:
        message_text = 'Активных заказов нет.'

    await bot.send_message(chat_id, message_text, reply_markup=fabrics.orders_insurer)



@router.callback_query(Mycallback.filter(F.action == 'принять'), Order.status)
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    data = await state.get_data()
    await bot.send_message(chat_id,
                           'Пожалуйста, приложите акт об осмотре в формате .pdf',
                           )
    time = data['time']

    # Изменено: используем UPDATE для обновления статуса по времени
    cursor.execute(
        'UPDATE orders SET status = ? WHERE time = ?',
        ('applied', time))

    conn.commit()
    await state.set_state(Order.applied)


@router.message(Order.applied, F.document)
async def get_doc(message: Message, state: FSMContext):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    doc_bytes = await bot.download_file(file.file_path)
    doc_bytes = doc_bytes.read()
    encoded_doc = base64.b64encode(doc_bytes).decode('utf-8')
    await state.update_data(doc=encoded_doc)
    data = await state.get_data()
    user_id = message.from_user.id
    time = data['time']

    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('UPDATE orders SET doc = ? WHERE time = ? ',
                   (encoded_doc, time))
    conn.commit()
    print("Акт осмотра успешно вставлен как BLOB в таблицу")

    # Получаем user_id из таблицы orders
    cursor.execute('SELECT user_id FROM orders WHERE time = ?', (time,))
    user_result = cursor.fetchone()
    user_to_send_id = user_result[0] if user_result else None

    user_id = message.from_user.id
    chat_id = message.chat.id
    data = await state.get_data()
    read_doc_data(time)

    # Отправляем сообщение пользователю
    if user_to_send_id:
        await bot.send_document(user_to_send_id, file_id, caption='Документ по заявке')
        await bot.send_message(user_to_send_id,
                               'Заявка принята. Акт осмотра направлен клиенту'
                               )


@router.callback_query(Mycallback.filter(F.action == 'отклонить'), Order.status)
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    data = await state.get_data()
    await bot.send_message(chat_id,
                           'Подробно опишите, что не соответствует установленным требованиям.',
                           reply_markup=fabrics.orders_insurer
                           )
    time = data['time']

    # Изменено: используем UPDATE для обновления статуса по времени
    cursor.execute(
        'UPDATE orders SET status = ? WHERE time = ?',
        ('rejected', time))

    conn.commit()
    await state.set_state(Order.rejected)


@router.message(Order.rejected)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(commentary=message.text)
    user_id = message.from_user.id
    chat_id = message.chat.id
    data = await state.get_data()
    await bot.send_message(chat_id,
                           'Заявка отклонена'
                           )
    time = data['time']
    commentary = data['commentary']
    # Изменено: используем UPDATE для обновления статуса по времени
    cursor.execute(
        'UPDATE orders SET commentary = ? WHERE time = ?',
        (commentary, time))

    conn.commit()
    await state.clear()


@router.callback_query(Mycallback.filter(F.action.startswith('админ')))
async def start_order(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    print('Зашли в обработчик')
    # Получаем действие из action
    action = callback_data.action

    if action.startswith('админ'):
        # Если действие связано с заявкой
        index = action.split('_')[-1]
        cursor.execute('SELECT DISTINCT time FROM orders')
        your_list_of_times = [row[0] for row in cursor.fetchall()]
        # Проверяем, что индекс находится в пределах допустимого диапазона
        if 1 <= int(index) <= len(your_list_of_times):
            # Получаем соответствующее время из your_list_of_times по индексу
            time = your_list_of_times[int(index) - 1]
            message_text = f'Вот ваша заявка от {time} из orders.'

            # Чтение и сохранение изображений из базы данных
            order_folder = read_blob_data(time)

            if order_folder:
                # Отправка фотографий пользователю
                await orders_insurer.send_photos_to_user(user_id, order_folder)

                await state.set_state(Order.status)
                await state.update_data(time=time)
        else:
            message_text = 'Некорректный индекс.'
    elif action == 'связаться':
        chat_id = call.message.chat.id

        # Ищем последнюю заявку в таблице orders
        cursor.execute('SELECT user_id, time FROM orders ORDER BY time DESC LIMIT 1')
        order_result = cursor.fetchone()
        message_text = 'Вы решили связаться с клиентом.'
        if order_result:
            user_id = order_result[0]

            # Ищем телефон в таблице users по user_id
            cursor.execute('SELECT phone, name, surname FROM users WHERE user_id = ?', (user_id,))
            phone_result = cursor.fetchone()

            if phone_result:
                phone = phone_result[0]
                name = phone_result[1]
                surname = phone_result[2]
                message_text = f'Контактный номер телефона пользователя {name} {surname}: {phone}'
                await state.set_state(Order.status)
            else:
                message_text = 'Телефон не найден.'
        else:
            message_text = 'Заявок не найдено.'

    else:
        # Действие не определено
        message_text = 'Неизвестное действие.'

    await bot.send_message(chat_id, message_text, reply_markup=fabrics.response_keyboard)


