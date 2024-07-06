from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str  # Токен для доступа к боту


@dataclass
class Config:
    tg_bot: TgBot


# Функция создания экземпляра класса Config
def load_config(path: str | None = None):
    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')
        )
    )

