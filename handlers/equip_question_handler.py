import logging
from aiogram import Router, F
from fsm_forms.fsm_models import FSMEquipForm
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from lexicon.lexicon_ru import (LEXICON_RU, HOME_TYPES, cancel_keyboard,
                                REPAIR_STAGE, yes_no_keyboard, LEXICON_MAIN_INLINE_RU)
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
    logger.info(f'Update handled by {start_form_equip.__name__}')


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
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер для обработки типа строения
@form_router.callback_query(FSMEquipForm.type_home)
async def set_type_home(callback: CallbackQuery, state: FSMContext):
    await state.update_data(home_type=callback.data)
    await state.set_state(FSMEquipForm.stage)
    await callback.message.edit_text(text=LEXICON_RU['stage'], reply_markup=get_other_keyboard(REPAIR_STAGE,
                                                                                               cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер на обработку ответа на этап строительства. Если ремонт завершен, то переходим на стейт one_button_count
@form_router.callback_query(FSMEquipForm.stage)
async def repair_stage(callback: CallbackQuery, state: FSMContext):
    await state.update_data(stage=callback.data)
    if callback.data == 'repair_complete':
        await state.update_data(wiring=None)
        await state.set_state(FSMEquipForm.one_button_switch)
        await callback.message.edit_text(text=LEXICON_RU['one_button_count'],
                                         reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await state.set_state(FSMEquipForm.wiring)
        await callback.message.edit_text(text=LEXICON_RU['wiring'], reply_markup=get_other_keyboard(yes_no_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндер обрабатывающий ответ на этап проводки электрики
@form_router.callback_query(FSMEquipForm.wiring)
async def wiring_stage(callback: CallbackQuery, state: FSMContext):
    await state.update_data(wiring=callback.data)
    if callback.data == 'yes':
        await state.set_state(FSMEquipForm.one_button_switch)
        await callback.message.edit_text(LEXICON_RU['one_button_count'],
                                         reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await state.set_state(FSMEquipForm.group_lights)
        await callback.message.edit_text(text=LEXICON_RU['group_lights'],
                                         reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на кол-во одноклавишных выключателей
@form_router.message(FSMEquipForm.one_button_switch)
async def one_button_switch(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(one_button_switch=int(message.text))
        await state.set_state(FSMEquipForm.two_button_switch)
        await message.answer(text=LEXICON_RU['two_button_count'], reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await message.answer(text=LEXICON_RU['button_count_false'], reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на кол-во двухклавишных выключателей
@form_router.message(FSMEquipForm.two_button_switch)
async def two_button_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(two_button_count=int(message.text))
        await state.set_state(FSMEquipForm.cross_button_existence)
        await message.answer(text=LEXICON_RU['cross_button_existence'], reply_markup=get_other_keyboard(yes_no_keyboard,
                                                                                                        cancel_keyboard))
    else:
        await message.answer(text=LEXICON_RU['button_count_false'], reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на наличие проходных и перекрёстных выключателей
@form_router.callback_query(FSMEquipForm.cross_button_existence)
async def cross_button_existence(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        await state.set_state(FSMEquipForm.cross_button_one)
        await callback.message.answer(text=LEXICON_RU['cross_button_one'],
                                      reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await state.set_state(FSMEquipForm.smart_socket)
        await callback.message.edit_text(text=LEXICON_RU['smart_socket_existence'],
                                         reply_markup=get_other_keyboard(yes_no_keyboard, cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на кол-во одноклавишных проходных выключателей
@form_router.message(FSMEquipForm.cross_button_one)
async def cross_button_one_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        if int(message.text) % 2 == 0:
            await state.update_data(cross_button_one_count=int(message.text))
            await state.set_state(FSMEquipForm.cross_button_two)
            await message.answer(text=LEXICON_RU['cross_button_two'], reply_markup=get_other_keyboard(cancel_keyboard))
        else:
            await message.answer(text=LEXICON_RU['cross_button_count_false'],
                                 reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await message.answer(text=LEXICON_RU['button_count_false'],
                             reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на кол-во двухклавишных проходных выключателей
@form_router.message(FSMEquipForm.cross_button_two)
async def cross_button_two_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        if int(message.text) % 2 == 0:
            await state.update_data(cross_button_two_count=int(message.text))
            await state.set_state(FSMEquipForm.cross_switch_one)
            await message.answer(text=LEXICON_RU['cross_switch_one'], reply_markup=get_other_keyboard(cancel_keyboard))
        else:
            await message.answer(text=LEXICON_RU['cross_button_count_false'],
                                 reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await message.answer(text=LEXICON_RU['button_count_false'],
                             reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на количество одноклавишных перекрёстных выключателей
@form_router.message(FSMEquipForm.cross_switch_one)
async def cross_switch_one_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(cross_switch_one_count=int(message.text))
        await state.set_state(FSMEquipForm.cross_switch_two)
        await message.answer(text=LEXICON_RU['cross_switch_two'], reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await message.answer(text=LEXICON_RU['button_count_false'], reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий отмену прохождения анкеты
@form_router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery, state=FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(text=LEXICON_RU['cancel'], reply_markup=get_other_keyboard(LEXICON_MAIN_INLINE_RU))
