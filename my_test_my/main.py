import requests
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.settings import settings


def main(geocode):
    apikey = settings.my_env.apikey
    lang = "ru_RU"

    url = f"https://geocode-maps.yandex.ru/1.x?apikey={apikey}&geocode={geocode}&lang={lang}&format=json"

    response = requests.get(url=url)

    if response.status_code == 200:
        data_json = response.json()
        # print(data_json)
        with open(
            f"C:\\DEV_python\\Test_Task\\Logik_Flask\\Flask_Project\\files_json\\{geocode}.json",
            "w",
            encoding="utf-8",
        ) as json_file:
            json.dump(data_json, json_file, ensure_ascii=False, indent=4)
    else:
        print("Ошибка", response.status_code)


if __name__ == "__main__":
    geocode = "Люберцы"
    main(geocode)
