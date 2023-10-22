from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram import types
from keyboards.fabrics import get_orders_list_insurer
from aiogram.filters.exception import ExceptionTypeFilter, ExceptionMessageFilter

import os

from aiogram.types import InputFile

import base64
import io

import datetime

from data.states import User, ExistUser, Neworderauto, Order
from data.states import Mycallback

from data.databases import db_table_val, conn, cursor, write_to_file, read_blob_data, read_doc_data

# Получение уникальных значений времени из таблицы 'orders'
cursor.execute('SELECT DISTINCT time FROM orders')
your_list_of_times = [row[0] for row in cursor.fetchall()]

from config_reader import config

from keyboards import reply, fabrics

router = Router()
bot = Bot(config.bot_token.get_secret_value())


@router.callback_query(Mycallback.filter(F.action == 'новые заявки страховщик'))
async def start_order(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    print("Обработчик для новых заявок страховщика сработал!")
    chat_id = call.message.chat.id

    # Получение всех уникальных времен из базы данных
    cursor.execute('SELECT DISTINCT time FROM orders WHERE status = ?', ('active',))
    your_list_of_times = [row[0] for row in cursor.fetchall()]

    if your_list_of_times:
        # Если есть времена, формируем сообщение
        message_text = f'На рассмотрение предлагаются следующие заявки:\n'
        for index, time in enumerate(your_list_of_times, start=1):
            message_text += f'Заявка от {time}\n'

        # Создаем клавиатуру с обновленным your_list_of_times
        orders_list_insurer = get_orders_list_insurer(your_list_of_times)
    else:
        message_text = 'Активных заказов нет.'
        orders_list_insurer = get_orders_list_insurer([])  # Пустой список времен
    await bot.edit_message_text(
        chat_id=str(chat_id),
        message_id=call.message.message_id,
        text=str(message_text),
        reply_markup=orders_list_insurer
    )


@router.callback_query(Mycallback.filter(F.action == 'история заявок страховщик'))
async def start_order(call: CallbackQuery, callback_data: Mycallback):
    chat_id = call.message.chat.id

    # Получение всех заказов из базы данных
    cursor.execute('SELECT orders.time, orders.status, users.name, users.surname '
                   'FROM orders '
                   'JOIN users ON orders.user_id = users.user_id')
    results = cursor.fetchall()

    if results:
        # Если есть заказы, формируем сообщение
        message_text = f'В базе данных присутствует информация о следующих заявках:\n'
        for row in results:
            if row[1] == 'active':
                message_text += f'Заявка от {row[0]} сформирована {row[2]} {row[3]}. Находится в состоянии "На рассмотрении"\n'
            if row[1] == 'rejected':
                message_text += f'Заявка от {row[0]} сформирована {row[2]} {row[3]}. Находится в состоянии "Отклонена"\n'
            # row - это кортеж, используйте индексы для доступа к значениям
            if row[1] == 'applied':
                message_text += f'Заявка от {row[0]} сформирована {row[2]} {row[3]}. Находится в состоянии "Принята"\n'
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
        await bot.send_document(user_to_send_id, file_id, caption=f'Акт осмотра по заявке, поданной Вами {time}')
        await bot.send_message(user_to_send_id,
                               f'Акт осмотра направлен клиенту.\n'
                           f'Отличная работа! Можете перейти к рассмотрению других заявок'
                               )


@router.callback_query(Mycallback.filter(F.action == 'отклонить'), Order.status)
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    data = await state.get_data()
    await bot.send_message(chat_id,
                           'Подробно опишите, что не соответствует установленным требованиям.'
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
                           f'Комментарий направлен клиенту.\n'
                           f'Отличная работа! Можете перейти к рассмотрению других заявок',
                           reply_markup=fabrics.orders_insurer
                           )
    time = data['time']
    commentary = data['commentary']
    # Изменено: используем UPDATE для обновления статуса по времени
    cursor.execute(
        'UPDATE orders SET commentary = ? WHERE time = ?',
        (commentary, time))

    conn.commit()
    await state.clear()

async def send_photos_to_user(user_id, order_folder):
    try:
        for filename in os.listdir(order_folder):
            if filename.endswith(".jpg"):
                photo_path = os.path.join(order_folder, filename)
                photo_file = FSInputFile(path = photo_path)
                await bot.send_photo(user_id, photo_file)
    except Exception as e:
        print(f"Ошибка при отправке фотографий: {e}")


@router.callback_query(Mycallback.filter())
async def start_order(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    print('Зашли в обработчик')
    # Получаем действие из action
    action = callback_data.action

    if action.startswith('заявка'):
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
                await send_photos_to_user(user_id, order_folder)

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
