import json

with open(
    r"C:\DEV_python\Test_Task\Logik_Flask\Flask_Project\files_json\Нижегородская обл. Кстово Паркова 7А.json",
    "r",
    encoding="utf8",
) as f:
    data = json.load(f)


def get_all_text_values(data):
    geo_object = data['response']['GeoObjectCollection']['featureMember']

    for i in geo_object:
        print(i['GeoObject'])


if __name__ == "__main__":
    print(get_all_text_values(data))
    # print(data['response']['GeoObjectCollection']['featureMember'])

    # print(data.get('text'))
