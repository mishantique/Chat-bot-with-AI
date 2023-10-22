from aiogram.types import Message, InputFile, FSInputFile
from aiogram.filters import Command
from aiogram import Router, Bot
from keyboards import reply, inline
from aiogram.fsm.context import FSMContext

from config_reader import config
bot = Bot(config.bot_token.get_secret_value())

router = Router()


@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await state.clear()
    logo = FSInputFile('data/logo.jpg')

    caption = f'Приветствуем Вас в сервисе для страхования транспортных средств и загородных домов от Совкомбанк Страхование. \n'\
              'Мы применяем в своей работе новейшие технологии, лучшие международные практики в сфере управления процессами и стремимся быть лучшими страховыми партнерами для наших клиентов.'

    await bot.send_photo(message.from_user.id, logo,
                         caption=caption,
                         reply_markup = reply.main)


@router.message(Command('menu'))
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f'Вы вернулись в главное меню',
        reply_markup = reply.main
        )


@router.message(Command('about'))
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f'Данный бот предназначен для ускорения процесса страхования объектов имущества. \n'
        f'С помощью бота Вы можете ознакомиться с регламентом, загрузить необходимые данные и создать заявку на страхование.',
        reply_markup = reply.main
        )

@router.message(Command('id'))
async def start(message: Message, state: FSMContext):
    #logo = FSInputFile('data/logo.jpg')
    await state.clear()
    #await bot.send_photo(chat_id=message.chat.id, photo=logo)
    await message.answer(
        f'Ваш id: {message.from_user.id}',
        reply_markup = reply.main
        )