import json
import logging
from pprint import pprint

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from lexicon.lexicon_ru import (LEXICON_RU, admin_main_menu, admin_menu_exit)
from keyboards.other_keyboards import get_other_keyboard
from lexicon.lexicon_ru import LEXICON_MAIN_INLINE_RU, admin_button
from aiogram import Bot

admin_router = Router()


# Хэнлер обрабатывающий выход из панели администратора
@admin_router.callback_query(F.data == 'exit_admin_menu')
async def exit_admin_menu(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await callback.answer(text=LEXICON_RU['admin_menu_exit'])
    await callback.message.delete()
    await bot.send_message(chat_id=callback.message.chat.id, text=LEXICON_RU['admin_main_menu'],
                           reply_markup=get_other_keyboard(LEXICON_MAIN_INLINE_RU, admin_button, width=1))


# Хэндлер отвечающий на кнопку "Панель администратора и отправляющий меню
@admin_router.callback_query(F.data == 'admin_panel', StateFilter(None))
async def admin_menu(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU['admin_main_menu'],
                                     reply_markup=get_other_keyboard(admin_main_menu, admin_menu_exit))
