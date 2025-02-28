from aiogram.fsm.state import StatesGroup, State

class Auth(StatesGroup):
    country = State()
    region = State()
    district = State()
    city = State()
    #links
    countryl = State()
    regionl = State()
    districtl = State()

class GetOneFish(StatesGroup):
    fishname = State()
    day = State()

class GetWeather(StatesGroup):
    day = State()