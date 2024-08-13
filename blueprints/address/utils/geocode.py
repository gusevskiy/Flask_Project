import json
import os
import sys

import requests
from loguru import logger

from blueprints.address.utils.log_config import setup_logger
from blueprints.address.utils.settings import settings

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

setup_logger()


def get_text_value(json_obj: dict) -> dict:
    """
    Ф-я принимает весь json обьект от API Геокодера
    Возвращает одну первую ноду данных по обьекту.
    """
    try:
        # Берем из структуры json только первый GeoObject, тк передпологаем что он у нас один
        # потому что есть валидация адресса в форме ввода.
        # Их может быть несколько если адрес указан не точно и вернется несколько похожиж локаций
        # по умочанию 10, можно указать опционально кол-во "results=5"
        geo_object = json_obj["response"]["GeoObjectCollection"]["featureMember"][0][
            "GeoObject"
        ]
        return geo_object
    except (IndexError, KeyError) as e:
        logger.error("Ошибка в структуре файла json", str(e))
        return None


def api_geocode(geocode: str) -> dict:
    """
    Ф-я принимает строку с адресом. Отправляет http запрос к сервису API Геокодера
    Пример:
        "Россия Москва Театральная 45"
    Возвращает:
        json обьект содержащий полную информацию об найденом адресе.
    """
    # получаем apikey от сервиса API Геокодер.
    apikey = settings.my_env.apikey
    lang = "ru_RU"

    url = f"https://geocode-maps.yandex.ru/1.x?apikey={apikey}&geocode={geocode}&lang={lang}&format=json"

    try:
        response = requests.get(url=url)
        response.raise_for_status()

        if response.status_code == 200:
            json_obj = response.json()
            # Возвращаем JSON
            return get_text_value(json_obj)
        else:
            logger.warning(
                "Статус ответа API геокодера не 200 = ", response.status_code
            )
            return None
    except requests.exceptions.RequestException as e:
        logger.error("Ошибка запроса к API Геокодера:", str(e))
