from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from data import data
from states import states
from parsers import fishparse
from kbs import keyboards
from . import someMethods
from templ import texttemplates
import re

fishrt = Router()

#one fish
@fishrt.callback_query(F.data == "onefishforecast")
async def oneFishForecast(callback: types.CallbackQuery, state: FSMContext):
    if data.checkUser(callback.from_user.id):
        await state.set_state(states.GetOneFish.fishname)
        await callback.message.edit_text("🎣Хорошо, введите название интересующей вас рыбы:")
    else:
        await callback.answer("⚠️Ошибка, пропишите /start")
    
@fishrt.message(states.GetOneFish.fishname)
async def fishNameIn(message: types.Message, state: FSMContext):
    if re.fullmatch(r'[А-Яа-яЁё,\\ -]+', message.text):
        fishname = await fishparse.oneFishCheck(data.getLink(message.from_user.id), message.text.lower(), message.from_user.id)
        if fishname:
            await state.update_data(fishname = fishname)
            await state.set_state(states.GetOneFish.day)
            await message.answer(f"🐟Ваша рыба: {fishname}\n🕔В какой день будете ловить?", reply_markup=keyboards.onefishMarkup)
        else:
            await message.answer("Похоже, тут не водится такой рыбы ⁉")
    else:
        await message.answer("⚠️Пожалуйста, введите имя рыбы на русском языке")
        
@fishrt.callback_query(states.GetOneFish.day)
async def fishDayIn(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(day = int(callback.data))
    datafu = await state.get_data()
    await state.clear()
    
    link = data.getLink(callback.from_user.id)
    if link == False:
        callback.answer('⚠️Ошибка, пропишите /start')
        return
    result = await fishparse.oneFishParser(link, datafu, callback.from_user.id)
    DAYFORMES = ['сегодня','завтра','послезавтра','через 2 дня','через 3 дня']
    
    if result:
        await callback.answer('')
        await callback.message.edit_text(f'🎣Шансы клёва {datafu['fishname']} {DAYFORMES[datafu['day']]}:\n\n🌙Ночью: {result[0][0]}% - {result[1][0]}\n🌅Утром: {result[0][1]}% - {result[1][1]}\n🌤️Днём: {result[0][2]}% - {result[1][2]}\n🌆Вечером: {result[0][3]}% - {result[1][3]} \n\n{result[2]}',
                                      reply_markup=keyboards.backMarkup)
    else:
        await callback.answer('⚠️Ошибка')
     
@fishrt.callback_query(F.data == 'fishback')
async def fishBack(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await someMethods.mainMenucb(callback)
  
#some fish  
@fishrt.callback_query(F.data == 'allfishforecast')
async def allFishForecast(callback: types.CallbackQuery, state: FSMContext):
    if data.checkUser(callback.from_user.id):
        link = data.getLink(callback.from_user.id)
        fishData = await fishparse.allFishParser(link, callback.from_user.id)
        fishlist = texttemplates.fishlist(fishData)
        await callback.message.edit_text(f"🦈Рыбы с лучшим клёвом сегодня в 📍{data.getCity(callback.from_user.id)}:\n{fishlist}\n\n 🎣Сможешь поймать всех?)",
                                        reply_markup=keyboards.backMarkup)
    else:
        await callback.answer("⚠️Ошибка, пропишите /start")