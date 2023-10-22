import os
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


from keyboards import inline, fabrics, reply
router = Router()

@router.message(F.text.in_(['Информация', 'Главное меню', 'Клиент', 'Администратор', 'Сотрудник']))
async def answer(message: Message, state: FSMContext):
    await state.clear()
    msg = message.text.lower()

    if msg == 'информация':
        await message.answer('Наши ссылки:', reply_markup = inline.link)

    if msg == 'главное меню':
        await message.answer('Вы вернулись в главное меню', reply_markup = reply.main)

    if msg == 'клиент':
        await message.answer('Пожалуйста, зарегистрируйтесь или авторизуйтесь', reply_markup = fabrics.auth_reg)

    if msg == 'администратор' and message.from_user.id == 539837691 or  msg == 'администратор' and message.from_user.id == 810350341:
        await message.answer('Вы авторизовались как администратор', reply_markup = reply.main_admin)

    if msg == 'администратор' and message.from_user.id != 539837691 and message.from_user.id != 810350341:
        await message.answer('Пожалуйста, согласуйте авторизацию с администрацией', reply_markup = reply.main)

    if msg == 'сотрудник':
        await message.answer('Пожалуйста, зарегистрируйтесь или авторизуйтесь', reply_markup = fabrics.auth_reg_insurer)



@router.message()
async def answer(message: Message, state: FSMContext):
    await state.clear()
    msg = message.text.lower()

    await message.answer('Неизвестная команда. Для получения информации, пожалуйста, введите команду "/about".')