from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types import Message, InputFile, FSInputFile

import datetime

from data.states import User, ExistUser, Neworderauto, Neworderhouse
from data.states import Mycallback

from data.databases import db_table_val, conn, cursor

from config_reader import config

from keyboards import reply, fabrics

import base64

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

@router.callback_query(Mycallback.filter(F.action == 'загородный дом'))
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    #await state.set_state(Neworder.opportunities)
    await bot.send_message(chat_id,
        'Ознакомьтесь с положениями', reply_markup = fabrics.opportunities_house
    )

@router.callback_query(Mycallback.filter(F.action == 'справка дом'))
async def start_reg(call: CallbackQuery, callback_data: Mycallback):
    chat_id = call.message.chat.id
    await bot.send_message(chat_id,
        f'Пожалуйста, ознакомьтесь с информацией.\n'
        f'В процессе проведения осмотра необходимо сделать следующие фотографии: \n'
        f'общий вид участка: несколько ракурсов участка для определения расстояний между объектами страхования, ограждением (забором), соседними сооружениями/зданиями, подъездными дорогами, объектами повышенного риска (стройка, водоемы и т.п.);\n'
        f'наружные инженерные коммуникации и сооружения: электроснабжения, водоснабжения, водоотведения, теплоснабжения, такие как: септик, эл.станция, трансформатор, распределительный щит, скважина, колодец, насос и т.п.;\n'
        f'фасады строений: каждое строение с 4-х сторон, элементы внешней отделки фасадов, кровлю, фундамент;\n'
        f'механическую защиту окон и дверей: наружные жалюзи, решетки и т.п. крупным планом, окна снаружи при отсутствии защиты;\n'
        f'входные (наружные) двери: с внешней стороны крупным планом;\n'
        f'внутреннее инженерное оборудование: сантехника, электрика (внутридомовой электрощит с автоматами в открытом виде), котел, бойлер, батареи, насос, камин,  кондиционер, емкости для топлива и/или воды и т.п. - крупным планом;\n'
        f'пожарную сигнализацию - все элементы крупным планом;\n'
        f'охранная сигнализация - все элементы крупным планом;', reply_markup = fabrics.opportunities_house1
    )


@router.callback_query(Mycallback.filter(F.action == 'требования к фотоматериалам дом'))
async def start_reg(call: CallbackQuery, callback_data: Mycallback):
    chat_id = call.message.chat.id
    await bot.send_message(chat_id,
        f'1. Фотография обязательно должна быть загружена в виде файла.\n'
        f'2. Обращаем Ваше внимание на то, что фотографии должны отображать реальное состояние объекта и не подвергаться обработки в фото-редакторах, в противном случае они могут быть отклонены.\n'
        f'3. Разрешение фотографии должно быть не ниже 1600*1200 px\n'
        f'4. Каждое фото должно содержать данные о дате, времени осмотра и геолокации объекта', reply_markup = fabrics.opportunities_house
    )

@router.callback_query(Mycallback.filter(F.action == 'загрузить фотографии дом'))
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    await state.set_state(Neworderhouse.photo1)
    await bot.send_message(chat_id,
        'Отправьте фото общего вида участка'
    )


@router.callback_query(Mycallback.filter(F.action == 'требования к фотоматериалам дом'))
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    #await state.set_state(Neworder.opportunities)
    await bot.send_message(chat_id,
        f'Пожалуйста, ознакомьтесь с требованиями к фотоматериалу:\n'
        f'1. Фотография обязательно должна быть загружена в виде файла.\n'
        f'2. Обращаем Ваше внимание на то, что фотографии должны отображать реальное состояние объекта и не подвергаться обработки в фото-редакторах, в противном случае они могут быть отклонены.\n'
        f'3. Разрешение фотографии должно быть не ниже 1600*1200 px\n'
        f'4. Каждое фото должно содержать данные о дате, времени осмотра и геолокации объекта.', reply_markup = fabrics.opportunities_house
    )

@router.callback_query(Mycallback.filter(F.action == 'добавить описание дом'))
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    await state.set_state(Neworderhouse.description)
    await bot.send_message(chat_id,
        'Пожалуйста, добавьте описание объекта. Укажите материал стен, количество комнат и другие характеристики.'
    )


@router.message(Neworderhouse.description, F.text)
async def add_description(message: Message, state: FSMContext):
    description = message.from_user
    await state.update_data(description=description)
    await message.answer(f'Спасибо! Пожалуйста, перейдите к загрузке фотоматериалов', reply_markup=fabrics.opportunities_house2)
    print("Описание сохранено для дальнейшего добавления в DB")



@router.message(Neworderhouse.photo1, F.photo)
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
    await state.update_data(photo1=message.photo[-1].file_id)
    await message.answer(f'Отправьте фото наружных инженерных коммуникаций')
    await state.set_state(Neworderhouse.photo2)


@router.message(Neworderhouse.photo2, F.photo)
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
    await message.answer(f'Отправьте фото фасада строения')
    await state.set_state(Neworderhouse.photo3)


@router.message(Neworderhouse.photo3, F.photo)
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
    await message.answer(f'Отправьте фотографию механической защита окон')
    await state.set_state(Neworderhouse.photo4)


@router.message(Neworderhouse.photo4, F.photo)
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
    await message.answer(f'Отправьте фотографию оконного блока')
    await state.set_state(Neworderhouse.photo5)


@router.message(Neworderhouse.photo5, F.photo)
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
    await message.answer(f'Отправьте фотографию входных дверей')
    await state.set_state(Neworderhouse.photo6)


@router.message(Neworderhouse.photo6, F.photo)
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
    await message.answer(f'Отправьте фотографию имеющихся дефектов или повреждений')
    await state.set_state(Neworderhouse.photo7)


@router.message(Neworderhouse.photo7, F.photo)
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
    await message.answer(f'Отправьте фотографию домашнего имущества')
    await state.set_state(Neworderhouse.photo8)


@router.message(Neworderhouse.photo8, F.photo)
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
    await message.answer(f'Отправьте фотографию забора')
    await state.set_state(Neworderhouse.photo9)


@router.message(Neworderhouse.photo9, F.photo)
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
    await message.answer(f'Отправьте фотографию внутреннего инженерного оборудования')
    await state.set_state(Neworderhouse.photo10)


@router.message(Neworderhouse.photo10, F.photo)
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
    await message.answer(f'Отправьте фотографию пожарной сигнализации')
    await state.set_state(Neworderhouse.photo11)


@router.message(Neworderhouse.photo11, F.photo)
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
    await message.answer(f'Отправьте фотографию охранной сигнализации')
    await state.set_state(Neworderhouse.photo12)


@router.message(Neworderhouse.photo12, F.photo)
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
    await message.answer(f'Отправьте фотографию внутренней отделки')
    await state.set_state(Neworderhouse.photo13)

#@router.message(Neworderhouse.photo14, F.photo)
#async def add_salon2_photo(message: Message, state: FSMContext):
    #await state.update_data(photo14=message.photo[-1].file_id)
    #await message.answer(f'На кузове есть повреждения?', reply_markup = fabrics.damage_auto)
    #await state.set_state(Neworderhouse.photo15)


#@router.callback_query(Mycallback.filter(F.action == 'повреждения есть'), Neworderhouse.photo15)
#async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    #chat_id = call.message.chat.id
    #await state.set_state(Neworderhouse.photo16)
    #await bot.send_message(chat_id,
        #'Отправьте фото повреждений'
    #)

#@router.callback_query(Mycallback.filter(F.action == 'повреждений нет'), Neworderhouse.photo15)
#async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    #chat_id = call.message.chat.id
    #await state.set_state(Neworderhouse.photo17)
    #await bot.send_message(chat_id,
        #f'У вас есть брелки?', reply_markup = fabrics.keys_auto
    #)

#@router.message(Neworderhouse.photo16, F.photo)
#async def add_salon2_photo(message: Message, state: FSMContext):
    #await state.update_data(photo16=message.photo[-1].file_id)
    #await message.answer(f'У вас есть брелки?', reply_markup = fabrics.keys_auto)
    #await state.set_state(Neworderhouse.photo17)

#@router.callback_query(Mycallback.filter(F.action == 'ключи есть'), Neworderhouse.photo17)
#async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    #chat_id = call.message.chat.id
    #await state.set_state(Neworderhouse.photo18)
    #await bot.send_message(chat_id,
        #'Отправьте фото ключей'
    #)

@router.message(Neworderhouse.photo13, F.photo)
async def add_salon2_photo(message: Message, state: FSMContext):
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
    await message.answer(f'При наличии прикрепите, пожалуйста, фотографию выписки из ЕГРН', reply_markup = fabrics.docs_house)
    await state.set_state(Neworderhouse.photo14)

@router.callback_query(Mycallback.filter(F.action == 'документ есть'), Neworderhouse.photo14)
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    await state.set_state(Neworderhouse.photo15)
    await bot.send_message(chat_id,
        'Отправьте фото документа'
    )

@router.callback_query(Mycallback.filter(F.action == 'документа нет'), Neworderhouse.photo14)
async def start_reg(call: CallbackQuery, callback_data: Mycallback, state: FSMContext):
    chat_id = call.message.chat.id
    house_plan = FSInputFile('data/house_plan.jpg')
    await state.set_state(Neworderhouse.photo15)
    await bot.send_photo(call.from_user.id, house_plan,
                         caption=f'Вам потребуется прикрепить нарисованную план-схему загородного дома в формате файла или фотографии. С примером Вы можете ознакомиться выше.\n'
        f'План-схема должна содержать следующую информацию:\n'
        f'расположение объектов на участке, включая расстояние между строениями относительно крайних точек объектов, расстояние от объектов до ограждения;\n'
        f'основные параметры объектов - внешние замеры длины, ширины, высоты;\n'
        f'привязка объектов к улице/дороге/к ограждению участка.',
                         )



@router.message(Neworderhouse.photo15, F.photo)
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
    print("Изображение 14 и данные успешно вставлены как BLOB и TEXT в таблицу")
    await state.update_data(photo15=message.photo[-1].file_id)
    user_id = message.from_user.id
    status = "active"
    await message.answer(f'Ваша заявка принята и скоро окажется на рассмотрении у страховщика. \n'
                         f'Вы можете отследить статус заявки в любое время',
                         reply_markup=fabrics.orders)
    await state.clear()
    # Обновление или вставка записи с использованием INSERT OR REPLACE
    cursor.execute('INSERT OR REPLACE INTO orders (user_id, time) VALUES (?, ?)',
                   (user_id, current_time))
    conn.commit()

