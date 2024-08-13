import unittest
from unittest.mock import MagicMock, patch

import requests
from flask import Flask
from flask.testing import FlaskClient

from blueprints.address.address import address
from blueprints.address.utils.geocode import api_geocode, get_text_value
from blueprints.address.utils.mkad import borders_mkad


class AddressTestCase(unittest.TestCase):
    def setUp(self):
        """
        Инициализируем Flask перед каждым тестом.
        """
        app = Flask(__name__)
        app.register_blueprint(address, url_prefix="/address")
        self.client = app.test_client()

    # start address
    def test_address_exists(self):
        """
        Адрес указан
        """
        response = self.client.post("/address/post_address", data="")
        self.assertEqual(response.status_code, 400)

    # end address
    # start geocode
    def test_get_text_value_success(self):
        """
        Проверка корректного извлечения данных из JSON.
        """
        json_obj = {
            "response": {
                "GeoObjectCollection": {
                    "featureMember": [
                        {
                            "GeoObject": {
                                "name": "Москва",
                                "Point": {"pos": "37.617633 55.755786"},
                            }
                        }
                    ]
                }
            }
        }

        expected_result = {"name": "Москва", "Point": {"pos": "37.617633 55.755786"}}

        result = get_text_value(json_obj)
        self.assertEqual(result, expected_result)

    @patch("blueprints.address.utils.geocode.requests.get")
    def test_api_geocode_success(self, mock_get):
        """
        Проверка успешного запроса к API Геокодера.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": {
                "GeoObjectCollection": {
                    "featureMember": [
                        {
                            "GeoObject": {
                                "name": "Москва",
                                "Point": {"pos": "37.617633 55.755786"},
                            }
                        }
                    ]
                }
            }
        }
        mock_get.return_value = mock_response

        address = "Россия Москва Театральная 45"
        result = api_geocode(address)

        expected_result = {"name": "Москва", "Point": {"pos": "37.617633 55.755786"}}

        self.assertEqual(result, expected_result)

    @patch("blueprints.address.utils.geocode.requests.get")
    def test_api_geocode_non_200_status(self, mock_get):
        """
        Проверка обработки некорректного статуса ответа API.
        """
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        address = "Россия Москва Театральная 45"
        result = api_geocode(address)

        self.assertIsNone(result)

    @patch("blueprints.address.utils.geocode.requests.get")
    def test_api_geocode_request_exception(self, mock_get):
        """
        Проверка обработки исключений при запросе к API.
        """
        # Эмитируем исключение при запросе
        mock_get.side_effect = requests.exceptions.RequestException

        address = "Россия Москва Театральная 45"
        result = api_geocode(address)

        self.assertIsNone(result)

    # end ceocode
    # start mkad
    def test_point_inside_mkad(self):
        """
        Проверка определения точки в пределах МКАД
        """
        # Эти координаты в пределах МКАД
        dict_point = {"pos": "37.79134874725341 55.68374100588486"}
        result = borders_mkad(dict_point)
        print(result)
        assert "находится в переделах МКАД." in result

    def test_point_outside_mkad(self):
        """
        Проверка определения точки за пределамии МКАД
        """
        # Эти координаты за пределами МКАД
        dict_point = {"pos": "37.9836094894409 55.67054905850316"}  #
        result = borders_mkad(dict_point)
        print(result)
        assert "растояние от МКАДА" in result and "км" in result
