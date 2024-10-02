from datetime import *
from tkinter import *
#Создаю окно
def open_window():
    window = Tk()
    window.geometry("500x500")
    window.title('Будильник')

    window.wm_attributes("-topmost", True)

    button = Button(window, text= "Stop", width=50, height= 50, command= window.destroy)
    button.pack(pady = 50)
    window.mainloop()

def validate_time(alarm_time):
    if len(alarm_time) !=5:
        return "wrong format"
    else:
        if int(alarm_time[0:2]) > 23:
            return "wrong format (hours)"
        elif int(alarm_time[3:5]) > 59:
            return "wrong format (min)"
        else:
            return "Done!"

while True:
    alarm_time = input("Введите время будильника в формате: \'HH:MM\' ")
    validate = validate_time(alarm_time)
    if validate != "Done!":
        print(validate)
    else:
        print(f"Будильник установлен на время {alarm_time}")
        break

alarm_hour = int(alarm_time[0:2])
alarm_min = int(alarm_time[3:5])

while True:
    now = datetime.now()
    current_hour = now.hour
    current_min = now.minute

    if alarm_hour == current_hour:
        if alarm_min == current_min:
            print("Настало время!")
            #Тут будет код, на высвечивание окошка с текстом
            open_window()
            break