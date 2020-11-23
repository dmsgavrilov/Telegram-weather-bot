import requests
import re
from bs4 import BeautifulSoup

_URL = "https://yandex.ru/pogoda/"
_TOWN = r'Прогноз погоды (во|в) (\w+)\b'
_TEMP = r"Текущая температура[+−]*(\d+)°"
_FEEL_LIKE = r"Ощущается как[+−]*(\d+)°"
_EXPECTED = r"картеВ (.)*Показать"
_WEATHER = r"°((\w)+( )*)*Ощущается"
_WIND = r'\d+,*\d+ м/с, \w{2}'

class WeatherBroadcast:
    town = "Moscow"
    def __init__(self, town):
        self.town = town

    def broadcast(self):
        req = requests.get(_URL + self.town)
        info = BeautifulSoup(req.text, "html.parser").get_text()
        get_town = re.search(_TOWN, info).group() + ':'
        get_temperature = re.search(_TEMP, info).group().replace('+', ': +').replace('−', ': −')
        get_felt_temperature = re.search(_FEEL_LIKE, info).group().replace('+', ' +').replace('−', ': −')
        get_weather = re.search(_WEATHER, info).group().replace('°', '').replace('Ощущается', '')
        get_wind = 'Ветер: ' + re.search(_WIND, info).group()
        try:
            get_expected = re.search(_EXPECTED, info).group().replace("картеВ", "В").replace("Показать", "")
        except:
            get_expected = ""
        return "\n".join([get_town, get_temperature, get_felt_temperature,  get_weather, get_wind, get_expected])

    def change_town(self, Newtown):
        self.town = Newtown

if __name__ == "__main__":
    req = requests.get(_URL + "Novosibirsk")
    info = BeautifulSoup(req.text, "html.parser").get_text()
