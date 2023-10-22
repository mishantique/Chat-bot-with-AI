from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Bot
import base64

import datetime

from data.states import User, ExistUser, Neworderauto
from data.states import Mycallback

from data.databases import db_table_val, conn, cursor

from config_reader import config

from keyboards import reply, fabrics

router = Router()
bot = Bot(config.bot_token.get_secret_value())

current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@router.callback_query(Mycallback.filter(F.action == 'подать заявку'))
async def start_order(call: CallbackQuery, callback_data: Mycallback):
    chat_id = call.message.chat.id
    await bot.send_message(chat_id,
        'Выберите тип объекта',
                           reply_markup = fabrics.order_type
    )

@router.callback_query(Mycallback.filter(F.action == 'автомобиль'))
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    #await state.set_state(Neworder.opportunities)
    await bot.send_message(chat_id,
        'Ознакомьтесь с положениями', reply_markup = fabrics.opportunities_auto
    )


@router.callback_query(Mycallback.filter(F.action == 'требования к фотоматериалам'))
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    #await state.set_state(Neworder.opportunities)
    await bot.send_message(chat_id,
        f'Пожалуйста, ознакомьтесь с требованиями к фотоматериалу:\n'
        f'1. Фотография обязательно должна быть загружена в виде файла.\n'
        f'2. Обращаем Ваше внимание на то, что фотографии должны отображать реальное состояние объекта и не подвергаться обработки в фото-редакторах, в противном случае они могут быть отклонены.\n'
        f'3. Разрешение фотографии должно быть не ниже 1600*1200 px.\n'
        f'4. Каждое фото должно содержать данные о дате, времени осмотра и геолокации объекта.', reply_markup = fabrics.opportunities_auto
    )


@router.callback_query(Mycallback.filter(F.action == 'справка'))
async def start_reg(call: CallbackQuery, callback_data: Mycallback):
    chat_id = call.message.chat.id
    await bot.send_message(chat_id,
        f'Пожалуйста, ознакомьтесь со справкой по загрузке фотоматериала: \n'
        f'1. Транспортное средство должно быть в чистом виде.\n'
        f'2. Не принимаются фото транспортного средства в разобранном виде или в процессе ремонта (установки противоугонных устройств и т.п.).\n'
        f'3. В процессе проведения осмотра необходимо сделать следующие фотографии:\n'
        f'фото VIN-номера на металле – минимум 1 фото;\n'
        f'фото транспортного средства снаружи – минимум 8 фото: с 4-х сторон + с 4-х углов (допускается больше при необходимости);\n'
        f'фото лобового стекла – минимум 1 фото;\n'
        f'фото маркировки лобового стекла – 1 фото;\n'
        f'фото колеса в сборе – минимум 1 фото (должны читаться размер и производитель шины);\n'
        f'фото показаний одометра (пробег) – 1 фото;\n'
        f'фото салона – минимум 2 фото: передняя часть салона с приборной панелью + задняя часть салона;\n'
        f'фото всех повреждений (при наличии) – неограниченное количество фото;\n'
        f'фото штатных ключей + ключей/брелоков/меток от дополнительных противоугонных устройств.', reply_markup = fabrics.opportunities_auto1
    )

@router.callback_query(Mycallback.filter(F.action == 'загрузить фотографии'))
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    await state.set_state(Neworderauto.photo1)
    await bot.send_message(chat_id,
        'Пожалуйста, отправьте фото VIN-номера на металле'
    )


@router.callback_query(Mycallback.filter(F.action == 'добавить описание'))
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    await state.set_state(Neworderauto.description)
    await bot.send_message(chat_id,
        'Пожалуйста, добавьте описание объекта. Укажите марку транспортного средства, год выпуска и технические характеристики'
    )



@router.message(Neworderauto.description, F.text)
async def add_description(message: Message, state: FSMContext):
    description = message.from_user
    await state.update_data(description=description)
    await message.answer(f'Спасибо! Пожалуйста, перейдите к загрузке фотоматериалов', reply_markup=fabrics.opportunities_auto2)
    print("Описание сохранено для дальнейшего добавления в DB")


@router.message(Neworderauto.photo1, F.photo)
async def add_first_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    photo_bytes = await bot.download_file(file.file_path)
    photo_bytes = photo_bytes.read()
    encoded_photo = base64.b64encode(photo_bytes).decode('utf-8')
    await state.update_data(photo1=encoded_photo)
    data = await state.get_data()
    user_id = message.from_user.id
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('INSERT OR REPLACE INTO orders (user_id, time, status, photo1) VALUES (?, ?, ?, ?)',
                   (user_id, current_time, 'active', encoded_photo))
    conn.commit()
    print("Изображение и данные успешно вставлены как BLOB и TEXT в таблицу")
    await message.answer(f'Отправьте первую фотографию транспортного средства снаружи')
    await state.set_state(Neworderauto.photo2)


@router.message(Neworderauto.photo2, F.photo)
async def add_second_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    photo_bytes = await bot.download_file(file.file_path)
    photo_bytes = photo_bytes.read()
    encoded_photo = base64.b64encode(photo_bytes).decode('utf-8')
    await state.update_data(photo2=encoded_photo)
    data = await state.get_data()
    user_id = message.from_user.id
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('UPDATE orders SET photo2 = ? WHERE time = ?', (encoded_photo, current_time))
    conn.commit()
    print("Изображение 2 и данные успешно вставлены как BLOB и TEXT в таблицу")
    await state.update_data(photo2=message.photo[-1].file_id)
    await message.answer(f'Отправьте вторую фотографию транспортного средства снаружи')
    await state.set_state(Neworderauto.photo3)


@router.message(Neworderauto.photo3, F.photo)
async def add_third_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    photo_bytes = await bot.download_file(file.file_path)
    photo_bytes = photo_bytes.read()
    encoded_photo = base64.b64encode(photo_bytes).decode('utf-8')
    await state.update_data(photo3=encoded_photo)
    data = await state.get_data()
    user_id = message.from_user.id
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('UPDATE orders SET photo3 = ? WHERE time = ?', (encoded_photo, current_time))
    conn.commit()
    print("Изображение 3 и данные успешно вставлены как BLOB и TEXT в таблицу")
    await state.update_data(photo3=message.photo[-1].file_id)
    await message.answer(f'Отправьте третью фотографию транспортного средства снаружи')
    await state.set_state(Neworderauto.photo4)


@router.message(Neworderauto.photo4, F.photo)
async def add_fourth_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    photo_bytes = await bot.download_file(file.file_path)
    photo_bytes = photo_bytes.read()
    encoded_photo = base64.b64encode(photo_bytes).decode('utf-8')
    await state.update_data(photo4=encoded_photo)
    data = await state.get_data()
    user_id = message.from_user.id
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('UPDATE orders SET photo4 = ? WHERE time = ?', (encoded_photo, current_time))
    conn.commit()
    print("Изображение 4 и данные успешно вставлены как BLOB и TEXT в таблицу")
    await state.update_data(photo4=message.photo[-1].file_id)
    await message.answer(f'Отправьте четветрую фотографию транспортного средства снаружи')
    await state.set_state(Neworderauto.photo5)


@router.message(Neworderauto.photo5, F.photo)
async def add_fifth_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    photo_bytes = await bot.download_file(file.file_path)
    photo_bytes = photo_bytes.read()
    encoded_photo = base64.b64encode(photo_bytes).decode('utf-8')
    await state.update_data(photo5=encoded_photo)
    data = await state.get_data()
    user_id = message.from_user.id
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('UPDATE orders SET photo5 = ? WHERE time = ?', (encoded_photo, current_time))
    conn.commit()
    print("Изображение 5 и данные успешно вставлены как BLOB и TEXT в таблицу")
    await state.update_data(photo5=message.photo[-1].file_id)
    await message.answer(f'Отправьте пятую фотографию транспортного средства снаружи')
    await state.set_state(Neworderauto.photo6)


@router.message(Neworderauto.photo6, F.photo)
async def add_sixth_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    photo_bytes = await bot.download_file(file.file_path)
    photo_bytes = photo_bytes.read()
    encoded_photo = base64.b64encode(photo_bytes).decode('utf-8')
    await state.update_data(photo6=encoded_photo)
    data = await state.get_data()
    user_id = message.from_user.id
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('UPDATE orders SET photo6 = ? WHERE time = ?', (encoded_photo, current_time))
    conn.commit()
    print("Изображение 6 и данные успешно вставлены как BLOB и TEXT в таблицу")
    await state.update_data(photo6=message.photo[-1].file_id)
    await message.answer(f'Отправьте шестую фотографию транспортного средства снаружи')
    await state.set_state(Neworderauto.photo7)


@router.message(Neworderauto.photo7, F.photo)
async def add_seventh_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    photo_bytes = await bot.download_file(file.file_path)
    photo_bytes = photo_bytes.read()
    encoded_photo = base64.b64encode(photo_bytes).decode('utf-8')
    await state.update_data(photo7=encoded_photo)
    data = await state.get_data()
    user_id = message.from_user.id
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('UPDATE orders SET photo7 = ? WHERE time = ?', (encoded_photo, current_time))
    conn.commit()
    print("Изображение 7 и данные успешно вставлены как BLOB и TEXT в таблицу")
    await state.update_data(photo7=message.photo[-1].file_id)
    await message.answer(f'Отправьте седьмую фотографию транспортного средства снаружи')
    await state.set_state(Neworderauto.photo8)


@router.message(Neworderauto.photo8, F.photo)
async def add_eight_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    photo_bytes = await bot.download_file(file.file_path)
    photo_bytes = photo_bytes.read()
    encoded_photo = base64.b64encode(photo_bytes).decode('utf-8')
    await state.update_data(photo8=encoded_photo)
    data = await state.get_data()
    user_id = message.from_user.id
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('UPDATE orders SET photo8 = ? WHERE time = ?', (encoded_photo, current_time))
    conn.commit()
    print("Изображение 8 и данные успешно вставлены как BLOB и TEXT в таблицу")
    await state.update_data(photo8=message.photo[-1].file_id)
    await message.answer(f'Отправьте восьмую фотографию транспортного средства снаружи')
    await state.set_state(Neworderauto.photo9)


@router.message(Neworderauto.photo9, F.photo)
async def add_window_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    photo_bytes = await bot.download_file(file.file_path)
    photo_bytes = photo_bytes.read()
    encoded_photo = base64.b64encode(photo_bytes).decode('utf-8')
    await state.update_data(photo9=encoded_photo)
    data = await state.get_data()
    user_id = message.from_user.id
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('UPDATE orders SET photo9 = ? WHERE time = ?', (encoded_photo, current_time))
    conn.commit()
    print("Изображение 9 и данные успешно вставлены как BLOB и TEXT в таблицу")
    await state.update_data(photo9=message.photo[-1].file_id)
    await message.answer(f'Отправьте фотографию лобового стекла')
    await state.set_state(Neworderauto.photo10)


@router.message(Neworderauto.photo10, F.photo)
async def add_window_marking_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    photo_bytes = await bot.download_file(file.file_path)
    photo_bytes = photo_bytes.read()
    encoded_photo = base64.b64encode(photo_bytes).decode('utf-8')
    await state.update_data(photo10=encoded_photo)
    data = await state.get_data()
    user_id = message.from_user.id
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('UPDATE orders SET photo10 = ? WHERE time = ?', (encoded_photo, current_time))
    conn.commit()
    print("Изображение 10 и данные успешно вставлены как BLOB и TEXT в таблицу")
    await state.update_data(photo10=message.photo[-1].file_id)
    await message.answer(f'Отправьте фотографию маркировки лобового стекла')
    await state.set_state(Neworderauto.photo11)


@router.message(Neworderauto.photo11, F.photo)
async def add_wheel_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    photo_bytes = await bot.download_file(file.file_path)
    photo_bytes = photo_bytes.read()
    encoded_photo = base64.b64encode(photo_bytes).decode('utf-8')
    await state.update_data(photo11=encoded_photo)
    data = await state.get_data()
    user_id = message.from_user.id
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('UPDATE orders SET photo11 = ? WHERE time = ?', (encoded_photo, current_time))
    conn.commit()
    print("Изображение 11 и данные успешно вставлены как BLOB и TEXT в таблицу")
    await state.update_data(photo11=message.photo[-1].file_id)
    await message.answer(f'Отправьте фотографию колеса в сборе')
    await state.set_state(Neworderauto.photo12)


@router.message(Neworderauto.photo12, F.photo)
async def add_odometer_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    photo_bytes = await bot.download_file(file.file_path)
    photo_bytes = photo_bytes.read()
    encoded_photo = base64.b64encode(photo_bytes).decode('utf-8')
    await state.update_data(photo12=encoded_photo)
    data = await state.get_data()
    user_id = message.from_user.id
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('UPDATE orders SET photo12 = ? WHERE time = ?', (encoded_photo, current_time))
    conn.commit()
    print("Изображение 12 и данные успешно вставлены как BLOB и TEXT в таблицу")
    await state.update_data(photo12=message.photo[-1].file_id)
    await message.answer(f'Отправьте фотографию показетелей одометра')
    await state.set_state(Neworderauto.photo13)


@router.message(Neworderauto.photo13, F.photo)
async def add_salon1_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    photo_bytes = await bot.download_file(file.file_path)
    photo_bytes = photo_bytes.read()
    encoded_photo = base64.b64encode(photo_bytes).decode('utf-8')
    await state.update_data(photo13=encoded_photo)
    data = await state.get_data()
    user_id = message.from_user.id
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('UPDATE orders SET photo13 = ? WHERE time = ?', (encoded_photo, current_time))
    conn.commit()
    print("Изображение 13 и данные успешно вставлены как BLOB и TEXT в таблицу")
    await state.update_data(photo13=message.photo[-1].file_id)
    await message.answer(f'Отправьте фотографию передней части салона автомобиля')
    await state.set_state(Neworderauto.photo14)


@router.message(Neworderauto.photo14, F.photo)
async def add_salon1_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    photo_bytes = await bot.download_file(file.file_path)
    photo_bytes = photo_bytes.read()
    encoded_photo = base64.b64encode(photo_bytes).decode('utf-8')
    await state.update_data(photo14=encoded_photo)
    data = await state.get_data()
    user_id = message.from_user.id
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('UPDATE orders SET photo14 = ? WHERE time = ?', (encoded_photo, current_time))
    conn.commit()
    print("Изображение 14 и данные успешно вставлены как BLOB и TEXT в таблицу")
    await state.update_data(photo14=message.photo[-1].file_id)
    await message.answer(f'Отправьте фотографию задней части салона автомобиля')
    await state.set_state(Neworderauto.photo15)


@router.message(Neworderauto.photo15, F.photo)
async def add_salon2_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    photo_bytes = await bot.download_file(file.file_path)
    photo_bytes = photo_bytes.read()
    encoded_photo = base64.b64encode(photo_bytes).decode('utf-8')
    await state.update_data(photo15=encoded_photo)
    data = await state.get_data()
    user_id = message.from_user.id
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('UPDATE orders SET photo15 = ? WHERE time = ?', (encoded_photo, current_time))
    conn.commit()
    print("Изображение 15 и данные успешно вставлены как BLOB и TEXT в таблицу")
    await state.update_data(photo15=message.photo[-1].file_id)
    await message.answer(f'На кузове есть повреждения?', reply_markup = fabrics.damage_auto)
    await state.set_state(Neworderauto.photo16)


@router.callback_query(Mycallback.filter(F.action == 'повреждения есть'), Neworderauto.photo16)
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    file_id = call.photo[-1].file_id
    file = await bot.get_file(file_id)
    photo_bytes = await bot.download_file(file.file_path)
    photo_bytes = photo_bytes.read()
    encoded_photo = base64.b64encode(photo_bytes).decode('utf-8')
    await state.update_data(photo16=encoded_photo)
    data = await state.get_data()
    user_id = call.from_user.id
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('UPDATE orders SET photo16 = ? WHERE time = ?', (encoded_photo, current_time))
    conn.commit()
    print("Изображение 16 и данные успешно вставлены как BLOB и TEXT в таблицу")
    chat_id = call.message.chat.id
    await state.set_state(Neworderauto.photo17)
    await bot.send_message(chat_id,
        'Отправьте фото повреждений'
    )

@router.callback_query(Mycallback.filter(F.action == 'повреждения отсутствуют'), Neworderauto.photo16)
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    await state.set_state(Neworderauto.photo18)
    await bot.send_message(chat_id,
        f'У вас есть брелки или  метки от противоугонных устройств?', reply_markup = fabrics.keys_auto
    )

@router.message(Neworderauto.photo17, F.photo)
async def add_salon2_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    photo_bytes = await bot.download_file(file.file_path)
    photo_bytes = photo_bytes.read()
    encoded_photo = base64.b64encode(photo_bytes).decode('utf-8')
    await state.update_data(photo17=encoded_photo)
    data = await state.get_data()
    description = data['description']
    user_id = message.from_user.id
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('INSERT OR REPLACE INTO orders (time, description) VALUES (?, ?)', (current_time, description))
    conn.commit()
    print("Изображение 17 и данные успешно вставлены как BLOB и TEXT в таблицу")
    await state.update_data(photo17=message.photo[-1].file_id)
    await message.answer(f'У вас есть брелоки или  метки от противоугонных устройств?', reply_markup = fabrics.keys_auto)
    await state.set_state(Neworderauto.photo17)

@router.callback_query(Mycallback.filter(F.action == 'ключи есть'), Neworderauto.photo18)
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    await state.set_state(Neworderauto.photo19)
    await bot.send_message(chat_id,
        'Отправьте фото'
    )

@router.message(Neworderauto.photo19, F.photo)
async def add_salon2_photo(message: Message, state: FSMContext):
    await state.update_data(photo19=message.photo[-1].file_id)
    user_id = message.from_user.id
    status = "active"
    await message.answer(f'Ваша заявка принята и скоро окажется на рассмотрении у страховщика. \n'
                         f'Вы можете отследить статус заявки в любое время',
                         reply_markup=fabrics.orders)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    import base64

    # Получаем данные из состояния
    data = await state.get_data()
    photos_data = [data.get(f'photo{i}', None) for i in range(1, 20)]  # Предполагается, что у вас есть 19 фотографий

    # Преобразуем фотографии в формат base64
    encoded_photos = [base64.b64encode(photo).decode('utf-8') if photo else None for photo in photos_data]
    cursor.execute('INSERT OR REPLACE INTO orders (user_id, time, status, photos) VALUES (?, ?, ?, ?)',
                   (user_id, current_time, status, encoded_photos))

    conn.commit()

    print('Фотографии успешно внесены в таблицу orders.')

    await state.clear()

@router.callback_query(Mycallback.filter(F.action == 'ключей нет'), Neworderauto.photo18)
async def add_order(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    status = 'active'
    await bot.send_message(chat_id, 'Ваша заявка принята и скоро окажется на рассмотрении у страховщика. Вы можете отследить статус заявки в любое время нажатием на кнопку "Узнать статус заявки"',
                         reply_markup=fabrics.orders)

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    #cursor.execute('INSERT OR REPLACE INTO orders (user_id, time, status) VALUES (?, ?, ?)',
                   #(user_id, current_time, status,))
    conn.commit()





