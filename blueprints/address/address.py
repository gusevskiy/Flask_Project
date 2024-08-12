from flask import Blueprint, request, jsonify
from loguru import logger
from utils.log_config import setup_logger


setup_logger()


address = Blueprint("address", __name__)


@address.route("/post_address", methods=["POST"])
def post_address():
    name = request.json
    print(name)
    # country = name.get('country')
    logger.info(name)
    return f"Hello, {name}!"
