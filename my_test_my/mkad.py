from shapely.geometry import Point, Polygon
from shapely.ops import nearest_points
import json


with open(r"C:\DEV_python\Test_Task\Logik_Flask\Flask_Project\my_test_my\mkad.json", "r") as f:
	data = json.load(f)

# Координаты контура МКАД (упрощенные, для примера)
mkad_coordinates = data["coordinates"][0]


# Создаем полигон МКАД
mkad_polygon = Polygon(mkad_coordinates)

# Пример точки (широта, долгота)
point_outside = Point(55.767305,37.976100)  # Точка в центре Москвы

# Проверка нахождения точки внутри МКАД
if mkad_polygon.contains(point_outside):
    print("Точка находится внутри МКАД")
else:
    # Находим ближайшую точку на границе МКАД
    nearest_point_on_mkad = nearest_points(mkad_polygon.boundary, point_outside)[0]
    print(f"Ближайшая точка на границе МКАД: {nearest_point_on_mkad.x}, {nearest_point_on_mkad.y}")
