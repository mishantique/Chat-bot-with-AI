from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Bot

from data.states import User, ExistUser
from data.states import Mycallback

from data.databases import db_table_val, conn, cursor

from config_reader import config

from keyboards import reply, fabrics

router = Router()
bot = Bot(config.bot_token.get_secret_value())

@router.callback_query(Mycallback.filter(F.action == 'авторизация'))
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    await state.clear()
    await state.set_state(ExistUser.login)
    await bot.send_message(chat_id,
        'Введите логин'
    )

@router.message(ExistUser.login)
async def check_name(message: Message, state: FSMContext):
    login = message.text
    # Проверка существования имени в базе данных
    cursor.execute('SELECT * FROM users WHERE login = ?', (login,))
    existing_user = cursor.fetchone()

    if existing_user:
        # Имя уже существует в базе данных, переход к запросу фамилии
        await message.answer(f'Напишите пароль')
        await state.update_data(login = login)
        await state.set_state(ExistUser.password)
    else:
        # Имя не существует в базе данных
        await message.answer(f'Учетная запись не обнаружена. Пожалуйста, зарегистрируйтесь',
                             reply_markup=reply.main)
        await state.clear()


@router.message(ExistUser.password)
async def check_name(message: Message, state: FSMContext):
    login_data = await state.get_data()
    login = login_data.get("login")
    password = message.text
    # Проверка существования имени в базе данных
    cursor.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, password))
    existing_user = cursor.fetchone()

    if existing_user:
        # Учетная запись есть, переход к функционалу
        await message.answer(f'Вы успешно авторизовались!', reply_markup=fabrics.orders)
    else:
        # Имя не существует в базе данных
        await message.answer(f'Неправильный пароль', reply_markup=reply.main)
        # await state.set_state(NewUser.surname)
        await state.clear()

