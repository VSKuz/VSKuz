import asyncio

from yaweather import Russia, YaWeatherAsync

async def main():
    async with YaWeatherAsync(api_key='d2f1a86c-fc13-4130-8172-910ebee4c7b5') as y:
        res = await y.forecast(Russia.Saratov, limit=2, hours=True)
        for f in res.forecasts:
            day = f.parts.day_short
            print(f'{f.date} {day.condition}, Температура днём {day.temp} °C, Ночью {f.parts.night_short.temp}')

asyncio.run(main())

# coordinates = [51.506544, 45.951417]
""" 
 if day.condition == {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
   'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
   'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
   'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
   'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
   'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
   'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'}
⛈🌤🌥🌧🌩☔⚡
"""