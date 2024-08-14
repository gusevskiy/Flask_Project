import json

from flask import Blueprint, jsonify, request
from loguru import logger

from blueprints.address.utils.log_config import setup_logger

from .utils.geocode import api_geocode
from .utils.mkad import borders_mkad

setup_logger()


address = Blueprint("address", __name__)


@address.route("/post_address", methods=["POST"])
def post_address():
    """
    Обработка запросов POST к маршруту /post_address.
    Принимает строку:
        curl --request POST --header "Content-Type: text/plain; charset=utf-8" --data "Ваш адрес" http://localhost:5000/address/post_address
    Blueprint:
        Часть адреса: "address"
    Возвращает string:
        "До адреса "Ваш адрес" растояние от МКАДА = 2.85 км"
    """
    try:
        address = request.data.decode("utf-8")  # Используем request.data для извлечения строки
        if not address or len(address) < 3:
            logger.error("address is None!")
            return "address is None!", 400
        logger.info("Получен адрес: ", address)
        geo_object = api_geocode(address)  # Отправляем на API Геокодера.
        # Из полученного json берем только Point среднию точку указанного адреса.
        point = geo_object["Point"]
        # logger.info(point)
        # Полученый словарь отправляем на определения нахождения относительно МКАД.
        distance = borders_mkad(point)
        logger.info(f"До адреса '{address}' {distance}")
        # Возвращаем результат, он возвращается в ответе на запрос.
        return f"До адреса '{address}' {distance}"
    except Exception as e:
        # Ловим общие ошибки по Blueprint.
        logger.error(f"Ошибка Blueprint {str(e)}")
        # Возвращаем для отображении в результате в форме.
        return "Internal server error", 400
