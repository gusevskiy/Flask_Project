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

# Пример использования
point1 = (55.767305,37.976100)  # Москва, Красная площадь
point2 = (55.771974101091104, 37.84262672750849)  # Санкт-Петербург, Дворцовая площадь

distance = haversine(point1, point2)
print(f"Расстояние: {distance:.2f} км")
