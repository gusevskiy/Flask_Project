## Flask_Project
------------------

### Модуль Flask Blueprint - расчитывает растояние от указанной точки на карте до МКАД по прямой использую формулу haversine.

#### Подключение blueprint "address"

Создайте папку в вашем проекте
```
mkdir ./bluprints/address
```
Слонируйте blueprint "address" в папку "address"
```
git clone https://github.com/gusevskiy/Flask_Project.git
```
Подключите blueprint "address" в вашем приложении
```
# app.py 
from blueprints.address.address import address

app.register_blueprint(address, url_prefix="/post_address")
```
После запуска приложения `flask run` blueprint `address` будет доступен по `http`
```
curl --request POST --header "Content-Type: application/json" --data '{"address": "your_address"}' http://localhost:5000/address/post_address
```
#### Используемые резурсы

[API Геокодера YAndex](https://yandex.ru/dev/geocode/doc/ru/request)  
[Примеры от яндекс на JS](https://yandex.ru/dev/maps/jsbox/2.1/multiroute_data_access)  
[Yandex карты кабинет разработчика](https://yandex.ru/maps-api/products/?from=club)  
[Flask](https://flask.palletsprojects.com/en/2.0.x/)  
[Для тестов получить адрес точки на карте с координатами](https://snipp.ru/tools/address-coord)  
