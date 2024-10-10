import requests
from tok import token


r = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={51.509666}&lon={45.957710}&appid={token}&units=metric&lang=ru')
data = r.json()
print(data)


def main():
    get_weather(token)


if __name__ == '__main__':
    main()

    """51.509666
    45.957710"""
