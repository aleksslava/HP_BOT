from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU


router = Router()

# Хендлер для команды /start
@router.message(Command(commands='start'))
async def process_start(message: Message):
    '''Отправка приветственного текста и главной клавиатуры'''

    await message.answer(text=LEXICON_RU['start'], )