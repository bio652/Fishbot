from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from data import data
from states import states
from . import someMethods

mainrt = Router()

@mainrt.message(Command('start'))
async def start(message: types.message, state: FSMContext):
    await state.clear()
    if data.checkUser(message.from_user.id):
        await someMethods.mainMenu(message, state)
    else:
        await state.set_state(states.Auth.country)
        await message.answer(f"👋Приветствую {message.from_user.first_name}!\n📍Для того чтобы помочь вам с рыбалкой мне нужно знать место где вы рыбачите!\n🌏Напишите мне свою страну:")