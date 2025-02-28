from aiogram import types, F
from aiogram.fsm.context import FSMContext

from data import data
from states import states
from kbs import keyboards

async def mainMenu(message: types.Message, state: FSMContext):
    await message.answer(f"👋Приветствую {message.from_user.first_name}!\n🦈Что хочешь узнать о рыбалке в 📍{data.getCity(message.from_user.id)}?",
                         reply_markup=keyboards.mainMarkup)
    
async def mainMenucb(callback: types.CallbackQuery):
    await callback.message.edit_text(f"👋Приветствую {callback.from_user.first_name}!\n🦈Что хочешь узнать о рыбалке в 📍{data.getCity(callback.from_user.id)}?",
                         reply_markup=keyboards.mainMarkup)

async def backtostart(message: types.message, state: FSMContext):
    await state.set_state(states.Auth.country)
    await message.answer(f"🌏Хорошо, сейчас введите свою страну:",reply_markup=keyboards.ReplyKeyboardRemove())