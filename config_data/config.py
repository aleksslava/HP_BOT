from environs import Env
from dataclasses import dataclass


# Класс с настройками бд
@dataclass
class DBSettings:
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # Функция генерирующая URL для подключения к бд
    @property
    def database_url_asyncpg(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


# Класс с токеном бота в телеграмм
@dataclass
class TgBot:
    token: str  # Токен для доступа к боту


# Класс объектом TGBot
@dataclass
class Config:
    tg_bot: TgBot
    admin_list: list[int]


# Функция создания экземпляра класса Config
def load_config(path: str | None = None):
    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')
        ),
        admin_list=[int(val) for val in env('ADMIN_LIST').split(sep=',')]
    )


# Функция создания класса настроек бд
def load_db_settings(path: str | None = None):
    env: Env = Env()
    env.read_env(path)

    return DBSettings(
        DB_HOST=env('DB_HOST'),
        DB_NAME=env('DB_NAME'),
        DB_PASS=env('DB_PASS'),
        DB_PORT=env('DB_PORT'),
        DB_USER=env('DB_USER')
    )
