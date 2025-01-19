#Таймер сделан для себя, с всплывающим окном
#Смысл в том, что я могу не уследить за временем за работой или просмотром ютюбчика,
#А всплывающее окно я не пропущу
from tkinter import *
import sys
import asyncio
import winsound

#Создаю окно для оповещения о том, что время вышло
def open_window():
    window = Tk()
    window.geometry("500x500")
    window.title('Таймер')

    window.wm_attributes("-topmost", True) #Оно будет открываться поверх остальных окон, чтобы не пропустить

    button = Button(window, text= "Stop", width=50, height= 50, command= window.destroy)
    button.pack(pady = 50)
    window.mainloop()

async def display_message():
    input_time = float(input("На сколько минут ставим таймер? "))
    print("Время установлено")
    # Переведём в секунды для удобства работы программы
    input_time = input_time * 60
    loop = asyncio.get_running_loop()
    end_time = loop.time() + input_time

    while True:
        remaining_time = end_time - loop.time()
        rt_min = remaining_time//60
        rt_sec = remaining_time - (rt_min * 60)
        if remaining_time <= 0:
            print("\nВремя вышло")
            winsound.MessageBeep() #Подать звуковой сигнал
            open_window()#Открыть оповещение
            break

        # Обновляем строку с оставшимся временем
        sys.stdout.write(f"\rОсталось {int(rt_min)}:{int(rt_sec)}")
        sys.stdout.flush()

        await asyncio.sleep(1)

asyncio.run(display_message())
