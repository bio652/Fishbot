from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

async def regdistkbbuilder(elements):
    builder = ReplyKeyboardBuilder()
    if len(elements) == 1:
       builder.add(KeyboardButton(text="↩️Предыдущий шаг↩️"))
       builder.add(KeyboardButton(text=elements[0]))
    else:
       builder.add(KeyboardButton(text="↩️Предыдущий шаг↩️"))   
       for i in range(0, len(elements)-1):
              builder.add(KeyboardButton(text=elements[i]))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

authcitybackMarkup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='↩️Предыдущий шаг↩️')]
], resize_keyboard=True)
 
mainMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🎣Узнать клёв определённой рыбы', callback_data="onefishforecast")],
    [InlineKeyboardButton(text='🐟Какая рыба может клюнуть', callback_data="allfishforecast")],
    [InlineKeyboardButton(text='⛅Узнать важные погодные данные', callback_data="getweather")],
    [InlineKeyboardButton(text='📍🔃Сменить локацию', callback_data="resetlocation")]
])

onefishMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🕔Сегодня', callback_data="0")],
    [InlineKeyboardButton(text='🕖Завтра', callback_data="1"),InlineKeyboardButton(text='🕖Послезавтра', callback_data="2")],
    [InlineKeyboardButton(text='🕚Через 2 дня', callback_data="3"),InlineKeyboardButton(text='🕚Через 3 дня', callback_data="4")]])

backMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🎣Узнать клёв другой рыбы', callback_data="onefishforecast")],
    [InlineKeyboardButton(text='↩️Вернуться', callback_data="fishback")]
])

resetMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📍🔃Сменить локацию', callback_data="resetTrue")],
    [InlineKeyboardButton(text='↩️Вернуться', callback_data="fishback")]
])

weatherMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🕔Сегодня', callback_data="0")],
    [InlineKeyboardButton(text='🕖Завтра', callback_data="1"),InlineKeyboardButton(text='🕖Послезавтра', callback_data="2")],
    [InlineKeyboardButton(text='🕚Через 2 дня', callback_data="3"),InlineKeyboardButton(text='🕚Через 3 дня', callback_data="4")],
    [InlineKeyboardButton(text='↩️Вернуться', callback_data="fishback")]])

weatherbackMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⛅Узнать Погоду в другой день', callback_data="getweather")],
    [InlineKeyboardButton(text='↩️Вернуться', callback_data="fishback")]
])