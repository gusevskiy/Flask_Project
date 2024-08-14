import json
import re

from flask import Blueprint, jsonify, request
from loguru import logger

from blueprints.address.utils.log_config import setup_logger

from .utils.geocode import api_geocode
from .utils.mkad import borders_mkad

setup_logger()


address = Blueprint("address", __name__)

MAX_ADDRESS_LENGTH = 255
MIN_ADDRESS_LENGTH = 5
ADDRESS_REGEX = re.compile(r'^[\w\s,.-]+$') 


@address.route("/post_address", methods=["POST"])
def post_address():
    """
    Обработка запросов POST к маршруту /post_address.
    Принимает данные:
        curl -X POST \
            -H "Content-Type: application/json" \
            -d '{"address": "Ваш адрес"}' \
            http://<host>:<port>/address/post_address
    Возвращает string:
        "До адреса "Ваш адрес" растояние от МКАДА = 2.85 км"
    """
    try:
        # обработка КОДИРОВОК тк curl запрос отправленный из windows в кодировке cp1251
        raw_data = request.get_data()
        try:
            data = raw_data.decode("utf-8")
            logger.debug(data)
        except UnicodeDecodeError as e:
            logger.info(f"Cannot decode data utf8 try in cp1251 {str(e)}")
            try:
                data = raw_data.decode("cp1251")
                logger.debug(data)
            except UnicodeDecodeError:
                logger.error("Cannot decode data")
                return jsonify({"error": "Cannot decode data"}), 400
        # Обработка JSON
        try:
            json_data = json.loads(data)
            logger.info(json_data)
        except json.JSONDecodeError:
            logger.error("Invalid JSON data")
            return jsonify({"error": "Invalid JSON data"}), 400
        # Получаем "адрес"
        try:
            address = json_data["address"]
            logger.info(address)
        except KeyError as e:
            logger.error("Key address not found")
            return ({"error": "Key address not found"})
        # Проверяем "адрес"
        if len(address) > MAX_ADDRESS_LENGTH:
            logger.error("Address too long")
            return jsonify({"error": "Address too long"}), 400

        if len(address) < MIN_ADDRESS_LENGTH:
            logger.error("Address too short")
            return jsonify({"error": "Address too short"}), 400

        if not ADDRESS_REGEX.match(address):
            logger.error("Invalid address format")
            return jsonify({"error": "Invalid address format"}), 400

        # print(address)
        geo_object = api_geocode(address)  # Отправляем на API Геокодера.
        # Из полученного json берем только Point среднию точку указанного адреса.
        point = geo_object["Point"]
        logger.info(point)
        # Полученый словарь отправляем на определения нахождения относительно МКАД.
        distance = borders_mkad(point)
        logger.info(f"До адреса '{address}' {distance}")
        # Возвращаем результат, он возвращается в ответе на запрос.
        return f"До адреса '{address}' {distance}"
        # return f"До адреса '{address}'"
    except Exception as e:
        # Ловим общие ошибки по Blueprint.
        logger.error(f"Ошибка Blueprint {str(e)}")
        # Возвращаем для отображении в результате в форме.
        return "Internal server error", 400
