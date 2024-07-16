import logging
from aiogram import Router, F
from fsm_forms.fsm_models import FSMEquipForm
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from lexicon.lexicon_ru import LEXICON_RU, HOME_TYPES, cancel_keyboard, REPAIR_STAGE
from keyboards.other_keyboards import get_other_keyboard


'''В данном модуле расположены хэндлеры на прохождение анкеты для подбора комплекта'''
logger = logging.getLogger(__name__)


form_router = Router()


# Хэндлер для обработки команды /equip, вход в анкету FSMEquipForm
@form_router.message(Command(commands='equip'), StateFilter(None))
async def start_form_equip(message: Message, state: FSMContext):
    await state.set_state(FSMEquipForm.name)
    await message.answer(text=LEXICON_RU['name'])
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер для обработки инлайн кнопки equip, вход в анкету FSMEquipForm
@form_router.callback_query(F.data == 'equip', StateFilter(None))
async def start_form_equip_inline(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMEquipForm.name)
    await callback.message.edit_text(text=LEXICON_RU['name'], reply_markup=get_other_keyboard(cancel_keyboard))


# Хэндлер для обработки имени клиента
@form_router.message(F.text, FSMEquipForm.name)
async def set_name(message: Message, state: FSMContext):
    if message.text.isalpha():
        await state.update_data(name=message.text)
        await state.set_state(FSMEquipForm.type_home)
        await message.answer(text=LEXICON_RU['type_home'], reply_markup=get_other_keyboard(HOME_TYPES,
                                                                                           cancel_keyboard, width=4))
    else:
        await message.answer(text=LEXICON_RU['name_false'], reply_markup=get_other_keyboard(cancel_keyboard))


# Хэндлер для обработки типа строения
@form_router.callback_query(FSMEquipForm.type_home)
async def set_type_home(callback:CallbackQuery, state: FSMContext):
    await state.update_data(home_type=callback.data)
    await state.set_state(FSMEquipForm.stage)
    await callback.message.edit_text(text=LEXICON_RU['stage'], reply_markup=get_other_keyboard(REPAIR_STAGE,
                                                                                               cancel_keyboard))


# Хэндлер обрабатывающий отмену прохождения анкеты
@form_router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery, state=FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(text=LEXICON_RU['cancel'])
