from flask import Blueprint, request, jsonify
from loguru import logger
from utils.log_config import setup_logger
from .utils_address.geocode import api_geocode
from .utils_address.mkad import borders_mkad


setup_logger()


address = Blueprint("address", __name__)


@address.route("/post_address", methods=["POST"])
def post_address():
    json_obj = request.json
    text_address = f"{json_obj.get('country')} {json_obj.get('region')} {json_obj.get('city')} {json_obj.get('street')} {json_obj.get('house')}"
    # print(text_address)
    geo_object = api_geocode(text_address)
    point = geo_object["Point"]

    res = borders_mkad(point)
    logger.info(f"До адреса '{text_address}' {res}")



    return f"Hello!"
