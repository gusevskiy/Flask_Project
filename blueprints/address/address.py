from flask import Blueprint, request, jsonify
import logging

address = Blueprint('address', __name__)

logging.basicConfig(level=logging.INFO)

@address.route('/post_address', methods=['POST'])
def post_address():
    name = request.json.get('name')
    logging.info(f"Received data: {name}")
    return f'Hello, {name}!'
