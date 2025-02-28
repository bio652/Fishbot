from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from data import data
from states import states
from parsers import authparse
from kbs import keyboards
from . import someMethods

authrt = Router()

@authrt.message(states.Auth.country)
async def authcountry(message: types.Message, state: FSMContext):
    if len(message.text) <= 20:
        countryLink = await authparse.countryCityParser(url="https://rybalku.ru/prognoz", datafc=message.text.strip().lower())
        if countryLink:
            await state.update_data(country = countryLink[0], countryl = countryLink[1])
            await state.set_state(states.Auth.region)
            regions = await authparse.RegDistKbParser(countryLink[1])
            await message.answer(f"🌏Ваша страна: {countryLink[0]}\n↩️Вы всегда можете вернуться на шаг назад.\n🚩Теперь укажите область/регион:", reply_markup= await keyboards.regdistkbbuilder(regions))
        else:
            await message.answer("⚠️Похоже, такой страны не существует, попробуйте ввести снова:")
    else:
        await message.answer("⚠️Введите коректнее)")

@authrt.message(states.Auth.region)
async def authregion(message: types.Message, state: FSMContext):
    if message.text == "↩️Предыдущий шаг↩️":
        await state.clear()
        await someMethods.backtostart(message, state)
        return
    curlink = await state.get_value('countryl')
    if message.text in await authparse.RegDistKbParser(curlink):
        regionLink = await authparse.RegDistLinkParser(curlink, message.text)
        await state.update_data(region = regionLink[0], curlink = regionLink[1], regionl = regionLink[1])
        await state.set_state(states.Auth.district)
        districts = await authparse.RegDistKbParser(regionLink[1])
        await message.answer(f"🚩Ваш регион: {message.text}\n↩️Вы всегда можете вернуться на шаг назад.\n📍Сейчас укажите район:",
                             reply_markup=await keyboards.regdistkbbuilder(districts))
    else:
        await message.answer("⚠️Пожалуйста, выбирете регион из списка")

async def backtoregion(message: types.message, state: FSMContext):
    curlink = await state.get_value('countryl')
    regions = await authparse.RegDistKbParser(curlink)
    await message.answer(f"↩️Предыдущий шаг\nВаша страна: {await state.get_value('country')}\n🚩Заново укажите область/регион:", reply_markup= await keyboards.regdistkbbuilder(regions))
    

@authrt.message(states.Auth.district)
async def authdistrict(message:types.Message, state: FSMContext):
    if message.text == "↩️Предыдущий шаг↩️":
        await state.set_state(states.Auth.region)
        await backtoregion(message, state)
        return
    curlink = await state.get_value('regionl')
    if message.text in await authparse.RegDistKbParser(curlink):
        districtLink = await authparse.RegDistLinkParser(curlink, message.text)
        await state.update_data(district = districtLink[0], curlink = districtLink[1], districtl = districtLink[1])
        await state.set_state(states.Auth.city)
        await message.answer(f"📍Ваш район: {message.text}\n↩️Вы всегда можете вернуться на шаг назад.\n🌆Введите ваш город/населенный пункт:",
                             reply_markup = keyboards.authcitybackMarkup)
    else:
        await message.answer("⚠️Пожалуйста, выбирете район из списка")

async def backtodist(message: types.message, state: FSMContext):
    curlink = await state.get_value('regionl')
    districts = await authparse.RegDistKbParser(curlink)
    await message.answer(f"↩️Предыдущий шаг\n📍Ваш регион: {await state.get_value('region')}\nЗаново укажите район:", reply_markup=await keyboards.regdistkbbuilder(districts))
       
@authrt.message(states.Auth.city)
async def authcity(message:types.Message, state: FSMContext):
    if message.text == "↩️Предыдущий шаг↩️":
        await state.set_state(states.Auth.district)
        await backtodist(message, state)
        return
    if len(message.text) <= 20:
        curlink = await state.get_value('districtl')
        cityLink = await authparse.countryCityParser(url=curlink, datafc=message.text.strip().lower())
        if cityLink:
            await state.update_data(city = cityLink[0])
            location = [await state.get_value('country'),await state.get_value('region'),await state.get_value('district'),await state.get_value('city')]
            print(location)
            result = data.addUser(userid=message.from_user.id, link=cityLink[1], location=location)
            if result:
                await state.clear()
                await message.answer(f"🌆Ваш населённый пункт: {cityLink[0]}\n🎉Вы прошли регистрацию!",reply_markup= keyboards.ReplyKeyboardRemove())
                await someMethods.mainMenu(message, state)
            else:
                await message.answer(f"⚠️Произошла неизвестная ошибка :(\nНачните заново - /start")   
        else:
            await message.answer("⚠️Похоже, такого города не существует, попробуйте ввести снова:")
    else:
        await message.answer("⚠️Введите коректнее)")

        
#reset location
@authrt.callback_query(F.data == "resetlocation")
async def resetLocation(callback: types.CallbackQuery):
    if data.checkUser(callback.from_user.id):
        await callback.message.edit_text(f"📍Вы сейчас находитесь в {data.getCity(callback.from_user.id)}\n⚠️Действительно хотите сменить локацию?",
            reply_markup=keyboards.resetMarkup)
    else:
        await callback.answer("⚠️Ошибка, пропишите /start")
    

@authrt.callback_query(F.data == "resetTrue")
async def reseting(callback: types.CallbackQuery):   
    result = data.resetUser(callback.from_user.id)
    if result:
        await callback.message.edit_text("✅Вы сбросили лоцкацию успешно!\nЕсли хотите установить новую - пропишите /start")
    else:
        await callback.answer("⚠️Произошла ошибка :(")
        await someMethods.mainMenucb(callback)