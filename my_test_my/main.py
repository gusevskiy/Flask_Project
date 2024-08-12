import requests
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.settings import settings


def get_text_value(data):
    if isinstance(data, dict):
        if "text" in data:
            return data["text"]
        for key, value in data.items():
            result = get_text_value(value)
            if result:
                return result
    elif isinstance(data, list):
        for item in data:
            result = get_text_value(item)
            if result:
                return result


def main(geocode):
    apikey = settings.my_env.apikey
    lang = "ru_RU"

    url = f"https://geocode-maps.yandex.ru/1.x?apikey={apikey}&geocode={geocode}&lang={lang}&format=json"

    response = requests.get(url=url)

    if response.status_code == 200:
        data_json = response.json()
        print(get_text_value(data_json))
    else:
        print("Ошибка", response.status_code)


if __name__ == "__main__":
    geocode = "Нижегородская обл. Кстово Паркова 7"
    main(geocode)
