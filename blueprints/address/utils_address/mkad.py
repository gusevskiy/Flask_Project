from shapely.geometry import Point, Polygon
from shapely.ops import nearest_points
import json
import math


def haversine(coord1, coord2):
    # Радиус Земли в километрах
    R = 6371.0

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Конвертируем градусы в радианы
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Разница координат
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Формула Haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Расстояние в километрах
    distance = R * c
    return distance


def borders_mkad(dict_point: dict):
    points_x = float(dict_point.get('pos').split()[1])
    points_y = float(dict_point.get('pos').split()[0])
    with open(r"C:\DEV_python\Test_Task\Logik_Flask\Flask_Project\my_test_my\mkad.json", "r") as f:
        data = json.load(f)

    mkad_coordinates = data["coordinates"][0]

    mkad_polygon = Polygon(mkad_coordinates)

    # # Пример точки (широта, долгота)
    point_outside = Point(points_x, points_y)

    # Проверка нахождения точки внутри МКАД
    if mkad_polygon.contains(point_outside):
        return "находится в переделах МКАД."
    else:
        # Находим ближайшую точку на границе МКАД
        nearest_point_on_mkad = nearest_points(mkad_polygon.boundary, point_outside)[0]
        coord_1 = (float(nearest_point_on_mkad.x), float(nearest_point_on_mkad.y))
        print(coord_1)
        coord_2 = (points_x, points_y)
        distance = haversine(coord_1, coord_2)
        return f"растояние от МКАДА = {distance:.2f} км"


if __name__ == '__main__':
    dict_point = {'pos': '37.99022 55.920038'}
    print(borders_mkad(dict_point))