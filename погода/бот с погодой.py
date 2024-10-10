from aiogram import Bot, Dispatcher, executor, types
from yaweather import Russia, YaWeather

bot = Bot(token='5863857574:AAFmimIqpJxeEaGX5JrO4qKnqp-wXSdw5X8')
dp = Dispatcher(bot)

@dp.message_handler()
async def echo(message: types.Message):
    y = YaWeather(api_key='d2f1a86c-fc13-4130-8172-910ebee4c7b5')
    res = y.forecast(Russia.Saratov, limit=2, hours=True)
    for f in res.forecasts:
        day = f.parts.day_short
        if day.condition == 'clear':
            day.condition = 'ясно ☀'
        elif day.condition == 'cloudy':
            day.condition = 'облачно ⛅'
        elif day.condition == 'overcast':
            day.condition = 'пасмурно ☁'
        elif day.condition == 'rain':
            day.condition = 'дождь 🌨'
        elif day.condition == 'snow ❄':
            day.condition = 'снег'
        elif day.condition == 'light-rain':
            day.condition = 'небольшой дождь 🌦'
        elif day.condition == 'snow-showers':
            day.condition = 'снегопад ❄❄❄'
        await message.answer(f'На {f.date}: Температура днём {day.temp} °C, ночью {f.parts.night_short.temp} °C, на улице {day.condition}')

if __name__ == '__main__':
     executor.start_polling(dp)

# if datetime.datetime ==