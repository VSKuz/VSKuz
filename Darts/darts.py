from colorama import Fore
#Задаём индивидуальный счёт для каждого игрока, равным итоговому счёту
score_1p = score_2p = int(input("До скольки играем? "))

while score_1p and score_2p != 0: #пока кто-то не выиграет
    while True:
        print(Fore.RED + "Ходит первый игрок!")
        dr1_1p = int(input("Сколько выбито первым дротиком? "))
        score_1p -= dr1_1p
        if score_1p == 0:
            print("Выиграл первый игрок!")
            break
        elif score_1p < 0:
            score_1p += dr1_1p
            print("Перебор, ход отменяется")
            print("У первого игрока ", score_1p, " очков")
            break
        print("У перврого игрока осталось ", score_1p, " очков")
        dr2_1p = int(input("Сколько выбито вторым дротиком? "))
        score_1p -= dr2_1p
        if score_1p == 0:
            print("Выиграл первый игрок!")
            break
        elif score_1p < 0:
            score_1p = score_1p + dr2_1p + dr1_1p
            print("Перебор, ход отменяется")
            print("У первого игрока ", score_1p, " очков")
            break
        print("У перврого игрока осталось ", score_1p, " очков")
        dr3_1p = int(input("Сколько выбито третим дротиком? "))
        score_1p -= dr3_1p
        if score_1p == 0:
            print("Выиграл первый игрок!")
            break
        elif score_1p < 0:
            score_1p = score_1p + dr3_1p + dr2_1p + dr1_1p
            print("Перебор, ход отменяется")
            print("У первого игрока ", score_1p, " очков")
            break
        print(Fore.YELLOW + "У перврого игрока осталось ", score_1p, " очков")
        break
    if score_1p == 0:
        continue
    while True:
        print(Fore.GREEN + "Ходит второй игрок!")
        dr1_2p = int(input("Сколько выбито первым дротиком? "))
        score_2p -= dr1_2p
        if score_2p == 0:
            print("Выиграл второй игрок!")
            break
        elif score_2p < 0:
            score_2p += dr1_2p
            print("Перебор, ход отменяется")
            print("У второго игрока ", score_2p, " очков")
            break
        print("У второго игрока осталось ", score_2p, " очков")
        dr2_2p = int(input("Сколько выбито вторым дротиком? "))
        score_2p -= dr2_2p
        if score_2p == 0:
            print("Выиграл второй игрок!")
            break
        elif score_2p < 0:
            score_2p = score_2p + dr2_2p + dr1_2p
            print("Перебор, ход отменяется")
            print("У второго игрока ", score_2p, " очков")
            break
        print("У второго игрока осталось ", score_2p, " очков")
        dr3_2p = int(input("Сколько выбито третим дротиком? "))
        score_2p -= dr3_2p
        if score_2p == 0:
            print("Выиграл второй игрок!")
            break
        elif score_2p < 0:
            score_2p = score_2p + dr3_2p + dr2_2p + dr1_2p
            print("Перебор, ход отменяется")
            print("У второго игрока ", score_2p, " очков")
            break
        print(Fore.YELLOW + "У второго игрока осталось ", score_2p, " очков")
        break
print(Fore.MAGENTA + "Ты самый меткий стрелок на Диком Западе, вообще супер-пупер зачётный пупсик дупсик чикиряу йоу камон!")
#Текст победы написан по заказу жены :D