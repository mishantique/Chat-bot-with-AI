from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Bot

from data.states import User, Insurer
from data.states import Mycallback

from data.databases import db_table_val, conn, cursor

from config_reader import config

from keyboards import fabrics

router = Router()
bot = Bot(config.bot_token.get_secret_value())

@router.callback_query(Mycallback.filter(F.action == 'регистрация сотрудник'))
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    await state.set_state(Insurer.unique_id)
    await bot.send_message(chat_id,
        'Введите уникальный идентификатор'
    )

@router.message(Insurer.unique_id)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(unique_id = message.text)
    await state.set_state(Insurer.login)
    await message.answer(
        'Введите логин'
    )

@router.message(Insurer.login)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(login = message.text)
    await state.set_state(Insurer.password)
    await message.answer(
        'Введите пароль'
    )

@router.message(Insurer.password)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(password = message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer(
        'Вы зарегистрировались',
        reply_markup = fabrics.auth_insurer
    )

    cursor.execute('INSERT INTO insurers (unique_id, login, password) VALUES (?, ?, ?)',
                   (data['unique_id'], data['login'], data['password']))
    conn.commit()