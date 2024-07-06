import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Инициализация логгера
logger = logging.getLogger(__name__)


async def main(storage: MemoryStorage | None = MemoryStorage()):
    # Конфигурируем логгер
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting Bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot: Bot = Bot(
        config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    logger.info('Bot started successful')


if __name__ == "__main__":
    asyncio.run(main())
