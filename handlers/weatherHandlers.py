from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from data import data
from states import states
from parsers import fishparse
from kbs import keyboards
from . import someMethods
from templ import texttemplates

weatherrt = Router()

@weatherrt.callback_query(F.data == "getweather")
async def getWeather(callback: types.CallbackQuery, state: FSMContext):
    if data.checkUser(callback.from_user.id):
        await state.set_state(states.GetWeather.day)
        await callback.message.edit_text("Погода за какой день интересует?", reply_markup=keyboards.weatherMarkup)
    else:
        await callback.answer("Ошибка, пропишите /start")
        
@weatherrt.callback_query(states.GetWeather.day, F.data != 'fishback')
async def getWeather(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    link = data.getLink(callback.from_user.id)
    day = int(callback.data)
    result = await fishparse.weatherParser(link, day, callback.from_user.id)
    DAYFORMES = ['сегодня','завтра','послезавтра','через 2 дня','через 3 дня']
    if result:
        if "NA" in result[1][0][1]:
            result[1][0][1] = "Порывов нету"
        if "NA" in result[1][1][1]:
            result[1][1][1] = "Порывов нету"
        if "NA" in result[1][2][1]:
            result[1][2][1] = "Порывов нету"
        if "NA" in result[1][3][1]:
            result[1][3][1] = "Порывов нету" 
        #sooo big message)   
        await callback.message.edit_text(f"""Важные погодные данные {DAYFORMES[day]}:
                                         
🌡 Температура воды:
 - Поверхность: {result[0][0]}°C,
 - Глубина: {result[0][1]}°C.
                                         
🌬 Ветер:
- 🌃 Ночью:
  - {result[1][0][0]}
  - {result[1][0][1]}
  - {result[1][0][2]}
  - 🌬 По направлению: {result[2][0]}
  
- 🌄 Утром:
  - {result[1][1][0]}
  - {result[1][1][1]}
  - {result[1][1][2]}
  - 🌬 По направлению: {result[2][1]}
  
- ⛅ Днём:
  - {result[1][2][0]}
  - {result[1][2][1]}
  - {result[1][2][2]}
  - 🌬 По направлению: {result[2][2]}
  
- ✨ Вечером:
  - {result[1][3][0]}
  - {result[1][3][1]}
  - {result[1][3][2]}
  - 🌬 По направлению: {result[2][3]}

🌙 Луна:
- {result[3]}
""", reply_markup=keyboards.weatherbackMarkup)
    else: 
        await callback.answer("Ошибка :(")