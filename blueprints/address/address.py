from flask import Blueprint, jsonify, request
from loguru import logger
import json
from utils.log_config import setup_logger

from .utils_address.geocode import api_geocode
from .utils_address.mkad import borders_mkad

setup_logger()


address = Blueprint("address", __name__)


@address.route("/post_address", methods=["POST"])
def post_address():
    """
    Обработка запросов POST к маршруту /post_address.
    Принимает JSON:
        curl --request POST --header "Content-Type: application/json" --data '{"address": "Москва, Центральный административный округ, район Хамовники, 461-й квартал"}' http://localhost:5000/address/post_address
    Blueprint:
        Часть адреса: "address"
    Возвращает:
        "До адреса 'Россия Московская область Мытищи Новомытищинский проспект 19А' растояние от МКАДА = 2.85 км"
    """
    try:
        # Декодируем кирилицу в cp1251 (utf8 не раскодирует тк разрабатываю на windows)
        raw_data = request.data.decode('cp1251')
        logger.debug(f"Decoded data: {raw_data}")

        json_data = json.loads(raw_data)
        json_obj = json_data.get('address')
        # Собираем полученый json в одно предложение.
        # text_address = f"{json_obj.get('country')} {json_obj.get('region')} {json_obj.get('city')} {json_obj.get('street')} {json_obj.get('house')}"
        # Отправляем на API Геокодера.
        geo_object = api_geocode(json_obj)
        # Из полученного json берем только Point среднию точку указанного адреса.
        point = geo_object["Point"]
        # Полученый словарь отправляем на определения нахождения относительно МКАД.
        res = borders_mkad(point)
        # Записываем ответ в лог файл.
        logger.info(f"До адреса '{json_obj}' {res}")
        # Возвращаем результат, он передается на страницу формы.
        return jsonify({"message": f"До адреса '{json_obj}' {res}"})
    except Exception as e:
        # Ловим общие ошибки по Blueprint.
        logger.error(f"Ошибка Blueprint {str(e)}")
        # Возвращаем для отображении в результате в форме.
        return jsonify({"error": "Internal server error"})