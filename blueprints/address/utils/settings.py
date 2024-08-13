from environs import Env
from dataclasses import dataclass


@dataclass
class MyEnv:
    apikey: str



@dataclass
class Settings:
    my_env: MyEnv


# ф-я формирования объекта настроеК
def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        my_env=MyEnv(
            apikey=env.str("APIKEY"),
        )
    )


# Считавем настройки из файла
settings = get_settings(".env")
# print(settings)  # test print