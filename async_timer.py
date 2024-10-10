import asyncio

async def display_message():
    input_time = float(input("На сколько минут ставим таймер? ")) #минуты для удобства пользователя
    #переведём в секунды для удобства работы программы
    input_time = input_time * 60 #тут можно было бы округлить ввод, но нет нужды
    loop = asyncio.get_running_loop()
    end_time = loop.time() + input_time
    while True:
        input_time -= 1
        print("Осталось", "%.0f" %input_time, "секунд")
        if (loop.time() + 1.0) >= end_time:
            print("Время вышло")
            break
        await asyncio.sleep(1)

asyncio.run(display_message())