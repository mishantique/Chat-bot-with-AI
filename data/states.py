from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State

class Mycallback(CallbackData, prefix="my"):
    action: str

class User(StatesGroup):
    name = State()
    surname = State()
    mail = State()
    login = State()
    password = State()
    phone = State()
    fill_db = State()


class Insurer(StatesGroup):
    login = State()
    password = State()
    unique_id = State()
    fill_db = State()



class ExistUser(StatesGroup):
    login = State()
    password = State()


class ExistInsurer(StatesGroup):
    unique_id = State()
    login = State()
    password = State()

class Order(StatesGroup):
    status = State()
    rejected = State()
    applied = State()
    push = State()

class Neworderauto(StatesGroup):
    description = State()
    photo1 = State()
    photo2 = State()
    photo3 = State()
    photo4 = State()
    photo5 = State()
    photo6 = State()
    photo7 = State()
    photo8 = State()
    photo9 = State()
    photo10 = State()
    photo11 = State()
    photo12 = State()
    photo13 = State()
    photo14 = State()
    photo15 = State()
    photo16 = State()
    photo17 = State()
    photo18 = State()
    photo19 = State()
    photo20 = State()
    confirm = State()
    complete_process = State()


class Neworderhouse(StatesGroup):
    photo1 = State()
    photo2 = State()
    photo3 = State()
    photo4 = State()
    photo5 = State()
    photo6 = State()
    photo7 = State()
    photo8 = State()
    photo9 = State()
    photo10 = State()
    photo11 = State()
    photo12 = State()
    photo13 = State()
    photo14 = State()
    photo15 = State()
    photo16 = State()
    photo17 = State()
    photo18 = State()
    description = State()

