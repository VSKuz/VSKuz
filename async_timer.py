#Таймер сделан для себя, с всплывающим окном
#Смысл в том, что я могу не уследить за временем за работой или просмотром ютюбчика,
#А всплывающее окно я не пропущу
from tkinter import *
import asyncio

#Создаю окно
def open_window():
    window = Tk()
    window.geometry("500x500")
    window.title('Таймер')

    window.wm_attributes("-topmost", True)

    button = Button(window, text= "Stop", width=50, height= 50, command= window.destroy)
    button.pack(pady = 50)
    window.mainloop()

async def display_message():
    input_time = float(input("На сколько минут ставим таймер? ")) #минуты для удобства пользователя
    print("Время установлено")
    #переведём в секунды для удобства работы программы
    input_time = input_time * 60 #тут можно было бы округлить ввод, но нет нужды
    loop = asyncio.get_running_loop()
    end_time = loop.time() + input_time
    while True:
        input_time -= 1
#Обратный отсчёт времени, если вдруг станет нужен, пусть будет
#        print("Осталось", "%.0f" %input_time, "секунд")
        if (loop.time() + 1.0) >= end_time:
            print("Время вышло")
            open_window()
            break
        await asyncio.sleep(1)

asyncio.run(display_message())
