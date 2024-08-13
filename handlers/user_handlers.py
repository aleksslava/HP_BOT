import logging

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon_ru import LEXICON_RU, LEXICON_MAIN_INLINE_RU, admin_keyboard
from keyboards.other_keyboards import get_other_keyboard
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from sqlalchemy import select
from sqlalchemy.orm.exc import MultipleResultsFound

logger = logging.getLogger(__name__)

router = Router()


# Хэндлер срабатывающий на команду /start
@router.message(Command(commands='start'), StateFilter(None))
async def process_start(message: Message, db: AsyncSession, admin_list: list):
    """Отправка приветственного текста и главной инлайн клавиатуры"""

    # Запрашиваем пользователя в бд
    db_response = await db.execute(select(User).where(User.tg_id == message.from_user.id))
    try:
        db_response = db_response.one_or_none()

        # Проверка есть ли пользователь в бд, если нет, добавляем.
        if db_response is None:
            user = User(name=message.from_user.first_name,
                        tg_id=message.from_user.id,
                        is_admin=message.from_user.id in admin_list)
            db.add(user)
            await db.commit()
        else:
            user = db_response[0]

        # Проверка пользователя на права администратора
        if user.is_admin:
            await message.answer(text='Администратор ' + user.name + LEXICON_RU['start'],
                                 reply_markup=get_other_keyboard(LEXICON_MAIN_INLINE_RU,
                                                                 admin_keyboard, width=1))
        else:
            await message.answer(text=user.name + LEXICON_RU['start'],
                                 reply_markup=get_other_keyboard(LEXICON_MAIN_INLINE_RU, width=1))

    # Отправка сообщения об ошибке
    except MultipleResultsFound as err:
        logger.error('В базе присутствует более одного пользователя с одним tg_id!')

        await message.answer(text=LEXICON_RU['err'])


# Хэндлер срабатывающий на команду /help
@router.message(Command(commands='help'), StateFilter(None))
async def process_help(message: Message):
    await message.answer(text=LEXICON_RU['help'], reply_markup=get_other_keyboard(LEXICON_MAIN_INLINE_RU))


# Хэндлер срабатывающий на инлайн кнопку Помощь
@router.callback_query(F.data == 'help', StateFilter(None))
async def process_inline_help(callback: CallbackQuery):
    if callback.message.text != LEXICON_RU['help']:
        await callback.message.edit_text(text=LEXICON_RU['help'], reply_markup=callback.message.reply_markup)
    else:
        await callback.answer(text=LEXICON_RU['repeat'])
