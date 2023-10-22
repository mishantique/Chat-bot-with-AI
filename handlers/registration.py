from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Bot
import re

from data.states import User
from data.states import Mycallback

from data.databases import db_table_val, conn, cursor

from config_reader import config

from keyboards import fabrics

router = Router()
bot = Bot(config.bot_token.get_secret_value())

@router.callback_query(Mycallback.filter(F.action == 'регистрация'))
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    await state.set_state(User.name)
    await bot.send_message(chat_id,
        'Как я могу к Вам обращаться? Пожалуйста, введите имя'
    )

@router.message(User.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(User.surname)
    await message.answer(
        'Пожалуйста, введите фамилию'
    )

@router.message(User.surname)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(surname = message.text)
    await state.set_state(User.mail)
    await message.answer(
        'Пожалуйста, ведите почту'
    )

@router.message(User.mail)
async def get_name(message: Message, state: FSMContext):
    if "@" in message.text:
        await state.update_data(mail = message.text)
        await state.set_state(User.login)
        await message.answer(
            'Введите логин'
        )
    else:
        await message.answer('Введите почту')

@router.message(User.login)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(login = message.text)
    await state.set_state(User.phone)
    await message.answer(
        'Пожалуйста, введите номер телефона в формате "+7(ххх)-ххх-хх-хх'
    )


@router.message(User.phone)
async def get_name(message: Message, state: FSMContext):
    phone = message.text.strip()

    # Проверка на соответствие формату номера телефона "+7(ххх)-ххх-хх-хх"
    phone_pattern = re.compile(r'^\+7\(\d{3}\)-\d{3}-\d{2}-\d{2}$')
    if not phone_pattern.match(phone):
        await message.answer('Пожалуйста, введите номер телефона в формате +7(ххх)-ххх-хх-хх')
        return

    await state.update_data(phone=phone)
    await state.set_state(User.password)
    await message.answer(
        f'Придумайте и введите надёжный пароль* \n'
        f'* Пароль должен содержать: \n'
        f'- не менее 6 символов \n'
        f'- минимум 1 цифру \n'
        f'- минимум 1 заглавную букву'
    )

@router.message(User.password)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    password = message.text.strip()

    # Проверка на соответствие условиям
    if not (len(password) >= 6 and any(c.isdigit() for c in password) and any(c.isupper() for c in password)):
        await message.answer(
            f'Неверный формат пароля. Пароль должен содержать:\n'
            f'- не менее 6 символов\n'
            f'- минимум 1 цифру\n'
            f'- минимум 1 заглавную букву'
        )
        return

    user_id = message.from_user.id
    data = await state.get_data()
    await state.clear()
    await message.answer(
        'Благодарим за регистрацию! \n'
        'Пожалуйста, авторизуйтесь, чтобы получить доступ к функционалу бота.',
        reply_markup=fabrics.auth
    )

    cursor.execute('INSERT INTO users (user_id, name, surname, mail, login, phone, password) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (user_id, data['name'], data['surname'], data['mail'], data['login'], data['phone'], data['password']))
    conn.commit()
