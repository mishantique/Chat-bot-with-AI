from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Bot

from data.states import User, ExistInsurer
from data.states import Mycallback

from data.databases import db_table_val, conn, cursor

from config_reader import config

from keyboards import reply, fabrics

router = Router()
bot = Bot(config.bot_token.get_secret_value())

@router.callback_query(Mycallback.filter(F.action == 'авторизация сотрудник'))
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    await state.clear()
    await state.set_state(ExistInsurer.unique_id)
    await bot.send_message(chat_id,
        'Введите идентификатор'
    )

@router.message(ExistInsurer.unique_id)
async def check_name(message: Message, state: FSMContext):
    unique_id = message.text
    # Проверка существования имени в базе данных
    cursor.execute('SELECT * FROM insurers WHERE unique_id = ?', (unique_id,))
    existing_insurer = cursor.fetchone()

    if existing_insurer:
        # Имя уже существует в базе данных, переход к запросу фамилии
        await message.answer(f'Напишите логин')
        await state.set_state(ExistInsurer.login)
        await state.update_data(unique_id=message.text)
    else:
        # Имя не существует в базе данных
        await message.answer(f'Идентификатор не обнаружен. Пожалуйста, согласуйте авторизацию',
                             reply_markup=reply.main)
        await state.clear()


@router.message(ExistInsurer.login)
async def check_name(message: Message, state: FSMContext):
    unique_id_data = await state.get_data()
    unique_id = unique_id_data.get("unique_id")
    await state.update_data(login=message.text)
    login = message.text
    # Проверка существования имени в базе данных
    cursor.execute('SELECT * FROM insurers WHERE unique_id = ? AND login = ?', (unique_id, login))
    existing_insurer = cursor.fetchone()

    if existing_insurer:
        # Учетная запись есть, переход к функционалу
        await message.answer(f'Введите пароль')
        await state.set_state(ExistInsurer.password)
    else:
        # Имя не существует в базе данных
        await message.answer(f'Неправильный логин', reply_markup=reply.main)
        # await state.set_state(NewUser.surname)
        await state.clear()


@router.message(ExistInsurer.password)
async def check_name(message: Message, state: FSMContext):
    login_data = await state.get_data()
    login = login_data.get("login")
    await state.update_data(password=message.text)
    password = message.text
    # Проверка существования имени в базе данных
    cursor.execute('SELECT * FROM insurers WHERE login = ? AND password = ?', (login, password))
    existing_insurer = cursor.fetchone()

    if existing_insurer:
        # Учетная запись есть, переход к функционалу
        await message.answer(f'Вы успешно авторизовались!', reply_markup = fabrics.orders_insurer)
    else:
        # Имя не существует в базе данных
        await message.answer(f'Неправильный пароль', reply_markup=reply.main)
        # await state.set_state(NewUser.surname)
        await state.clear()

