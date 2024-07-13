
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon_ru import LEXICON_RU, LEXICON_MAIN_INLINE_RU
from keyboards.main_menu_keyboard import inline_main_menu


router = Router()


# Хэндлер срабатывающий на команду /start
@router.message(Command(commands='start'))
async def process_start(message: Message):
    """Отправка приветственного текста и главной инлайн клавиатуры"""

    await message.answer(text=LEXICON_RU['start'], reply_markup=inline_main_menu(LEXICON_MAIN_INLINE_RU))


# Хэндлер срабатывающий на команду /help
@router.message(Command(commands='help'))
async def process_help(message: Message):
    await message.answer(text=LEXICON_RU['help'], reply_markup=inline_main_menu(LEXICON_MAIN_INLINE_RU))


# Хэндлер срабатывающий на инлайн кнопку Помощь
@router.callback_query(F.data == 'help')
async def process_inline_help(callback: CallbackQuery):
    if callback.message.text != LEXICON_RU['help']:
        await callback.message.edit_text(text=LEXICON_RU['help'], reply_markup=callback.message.reply_markup)
    else:
        await callback.answer(text=LEXICON_RU['repeat'])


