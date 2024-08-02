import logging
from pprint import pprint

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

# Хэндлер обрабатывающий отмену прохождения анкеты
@form_router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery, state=FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(text=LEXICON_RU['cancel'], reply_markup=get_other_keyboard(LEXICON_MAIN_INLINE_RU))


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
                                                                                           cancel_keyboard, width=1))
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
        await state.update_data(wiring=True)
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
        await state.update_data(cross_button_existence=True)
        await state.set_state(FSMEquipForm.cross_button_one)
        await callback.message.edit_text(text=LEXICON_RU['cross_button_one'],
                                         reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await state.update_data(cross_button_existence=False)
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


# Хэндлер обрабатывающий ответ на кол-во двухклавишных перекрестных выключателей
@form_router.message(FSMEquipForm.cross_switch_two)
async def cross_switch_two_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(cross_switch_two_count=int(message.text))
        await state.set_state(FSMEquipForm.smart_socket)
        await message.answer(text=LEXICON_RU['smart_socket_existence'],
                             reply_markup=get_other_keyboard(yes_no_keyboard, cancel_keyboard))
    else:
        await message.answer(text=LEXICON_RU['button_count_false'], reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на общее количество групп света
@form_router.message(FSMEquipForm.group_lights)
async def group_lights_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(group_lights_count=int(message.text))
        await state.set_state(FSMEquipForm.led_strips)
        await message.answer(text=LEXICON_RU['led_strips_existence'],
                             reply_markup=get_other_keyboard(yes_no_keyboard, cancel_keyboard))
    else:
        await message.answer(LEXICON_RU['button_count_false'], reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на наличие led лент
@form_router.callback_query(FSMEquipForm.led_strips)
async def led_strips_existence(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        await state.update_data(led_existence=True)
        await state.set_state(FSMEquipForm.led_strips_count)
        await callback.message.edit_text(text=LEXICON_RU['led_strips_count'],
                                         reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await state.update_data(led_existence=False)
        await state.set_state(FSMEquipForm.smart_socket)
        await callback.message.edit_text(text=LEXICON_RU['smart_socket_existence'],
                                         reply_markup=get_other_keyboard(yes_no_keyboard, cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')



# Хэндлер обрабатывающий ответ на количество одноцветных led лент
@form_router.message(FSMEquipForm.led_strips_count)
async def led_strips_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(led_strips_count=int(message.text))
        await state.set_state(FSMEquipForm.rgb_strips_count)
        await message.answer(text=LEXICON_RU['rgb_strips_count'], reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await message.answer(text=LEXICON_RU['button_count_false'], reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на количество rgb лент
@form_router.message(FSMEquipForm.rgb_strips_count)
async def rgb_strips_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(rgb_strips_count=int(message.text))
        await state.set_state(FSMEquipForm.rgbw_strips_count)
        await message.answer(text=LEXICON_RU['rgbw_strips_count'], reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await message.answer(text=LEXICON_RU['button_count_false'], reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на количество rgbw лент
@form_router.message(FSMEquipForm.rgbw_strips_count)
async def rgbw_strips_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(rgbw_strips_count=int(message.text))
        await state.set_state(FSMEquipForm.dim_lights)
        await message.answer(text=LEXICON_RU['dim_lights_existence'],
                             reply_markup=get_other_keyboard(yes_no_keyboard, cancel_keyboard))
    else:
        await message.answer(text=LEXICON_RU['button_count_false'], reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на наличие диммируемых групп освещения
@form_router.callback_query(FSMEquipForm.dim_lights)
async def dim_lights_existence(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        await state.update_data(dim_lights_existence=True)
        await state.set_state(FSMEquipForm.dim_lights_count)
        await callback.message.edit_text(text=LEXICON_RU['dim_lights_count'],
                                         reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await state.update_data(dim_lights_existence=False)
        await state.set_state(FSMEquipForm.smart_socket)
        await callback.message.edit_text(text=LEXICON_RU['smart_socket_existence'],
                                         reply_markup=get_other_keyboard(yes_no_keyboard, cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на количество диммируемых групп освещения
@form_router.message(FSMEquipForm.dim_lights_count)
async def dim_lights_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(dim_lights_count=int(message.text))
        await state.set_state(FSMEquipForm.smart_socket)
        await message.answer(text=LEXICON_RU['smart_socket_existence'],
                             reply_markup=get_other_keyboard(yes_no_keyboard, cancel_keyboard))
    else:
        await message.answer(text=LEXICON_RU['button_count_false'], reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на наличие умных розеток
@form_router.callback_query(FSMEquipForm.smart_socket)
async def smart_socket_existence(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        await state.update_data(smart_socket_existence=True)
        await state.set_state(FSMEquipForm.smart_socket_count)
        await callback.message.edit_text(text=LEXICON_RU['smart_socket_count'],
                                         reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await state.update_data(smart_socket_existence=False)
        await state.set_state(FSMEquipForm.water_protect)
        await callback.message.edit_text(text=LEXICON_RU['water_protect'],
                                         reply_markup=get_other_keyboard(yes_no_keyboard, cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндел обрабатывающий ответ на количество умных розеток
@form_router.message(FSMEquipForm.smart_socket_count)
async def smart_socket_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(smart_socket_count=int(message.text))
        await state.set_state(FSMEquipForm.water_protect)
        await message.answer(text=LEXICON_RU['water_protect'],
                             reply_markup=get_other_keyboard(yes_no_keyboard, cancel_keyboard))
    else:
        await message.answer(text=LEXICON_RU['button_count_false'], reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на необходимость защиты от протечек
@form_router.callback_query(FSMEquipForm.water_protect)
async def water_protect_existence(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        await state.update_data(water_protect_existence=True)
        await state.set_state(FSMEquipForm.wet_zone_count)
        await callback.message.edit_text(text=LEXICON_RU['wet_zone_count'],
                                         reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await state.update_data(water_protect_existence=False)
        await state.set_state(FSMEquipForm.smart_cornice_existence)
        await callback.message.edit_text(text=LEXICON_RU['smart_cornice_existence'],
                                         reply_markup=get_other_keyboard(yes_no_keyboard, cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на количество мокрых зон
@form_router.message(FSMEquipForm.wet_zone_count)
async def wet_zone_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(wet_zone_count=int(message.text))
        await state.set_state(FSMEquipForm.water_rizer_count)
        await message.answer(text=LEXICON_RU['water_rizer_count'],
                             reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await message.answer(text=LEXICON_RU['button_count_false'], reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на количество стояков системы водоснабжения
@form_router.message(FSMEquipForm.water_rizer_count)
async def water_rizer_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(water_rizer_count=int(message.text))
        await state.set_state(FSMEquipForm.smart_cornice_existence)
        await message.answer(text=LEXICON_RU['smart_cornice_existence'],
                             reply_markup=get_other_keyboard(yes_no_keyboard, cancel_keyboard))
    else:
        await message.answer(text=LEXICON_RU['button_count_false'], reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на необходимость электрокарнизов
@form_router.callback_query(FSMEquipForm.smart_cornice_existence)
async def smart_cornice_existence(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        await state.update_data(smart_cornice_existence=True)
        await state.set_state(FSMEquipForm.smart_cornice_count)
        await callback.message.edit_text(text=LEXICON_RU['smart_cornice_count'],
                                         reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await state.update_data(smart_cornice_existence=False)
        await state.set_state(FSMEquipForm.warm_floor_electric)
        await callback.message.edit_text(text=LEXICON_RU['warm_floor_electric'],
                                         reply_markup=get_other_keyboard(yes_no_keyboard, cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на количество электрокарнизов
@form_router.message(FSMEquipForm.smart_cornice_count)
async def smart_cornice_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(smart_cornice_count=int(message.text))
        await state.set_state(FSMEquipForm.warm_floor_electric)
        await message.answer(text=LEXICON_RU['warm_floor_electric'],
                             reply_markup=get_other_keyboard(yes_no_keyboard, cancel_keyboard))
    else:
        await message.answer(text=LEXICON_RU['button_count_false'], reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на необходимость электического тёплого пола
@form_router.callback_query(FSMEquipForm.warm_floor_electric)
async def warm_floor_electric(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        await state.update_data(warm_floor_electric=True)
        await state.set_state(FSMEquipForm.warm_floor_electric_count)
        await callback.message.edit_text(text=LEXICON_RU['warm_floor_electric_count'],
                                         reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await state.update_data(smart_cornice_existence=False)
        await state.set_state(FSMEquipForm.warm_floor_water)
        await callback.message.edit_text(text=LEXICON_RU['warm_floor_water'],
                                         reply_markup=get_other_keyboard(yes_no_keyboard, cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на количество зон электрического тёплого пола
@form_router.message(FSMEquipForm.warm_floor_electric_count)
async def warm_floor_electric_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(warm_floor_electric_count=int(message.text))
        await state.set_state(FSMEquipForm.warm_floor_water)
        await message.answer(text=LEXICON_RU['warm_floor_water'],
                             reply_markup=get_other_keyboard(yes_no_keyboard, cancel_keyboard))
    else:
        await message.answer(text=LEXICON_RU['button_count_false'], reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на необходимость водяного тёплого пола
@form_router.callback_query(FSMEquipForm.warm_floor_water)
async def warm_floor_water(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        await state.update_data(warm_floor_water=True)
        await state.set_state(FSMEquipForm.warm_floor_water_count)
        await callback.message.edit_text(text=LEXICON_RU['warm_floor_water_count'],
                                         reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await state.update_data(warm_floor_water=False)
        data = await state.get_data()
        if data['home_type'] == 'cottage':
            await state.set_state(FSMEquipForm.smart_gates)
            await callback.message.edit_text(text=LEXICON_RU['smart_gates'],
                                             reply_markup=get_other_keyboard(yes_no_keyboard, cancel_keyboard))
        else:
            await state.clear()
            await callback.message.edit_text(text='Тут будет отправляться список оборудования',
                                             reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на количество зон водяного теплого пола
@form_router.message(FSMEquipForm.warm_floor_water_count)
async def warm_floor_water_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(warm_floor_water_count=int(message.text))
        data = await state.get_data()
        if data['home_type'] == 'cottage':
            await state.set_state(FSMEquipForm.smart_gates)
            await message.answer(text=LEXICON_RU['smart_gates'],
                                    reply_markup=get_other_keyboard(yes_no_keyboard, cancel_keyboard))
        else:
            await state.clear()
            await message.answer(text='Тут будет отправляться список оборудования',
                                    reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на необходимость подключения ворот
@form_router.callback_query(FSMEquipForm.smart_gates)
async def smart_gates(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        await state.update_data(smart_gates=True)
        await state.set_state(FSMEquipForm.smart_gates_count)
        await callback.message.edit_text(text=LEXICON_RU['smart_gates_count'],
                                         reply_markup=get_other_keyboard(cancel_keyboard))
    else:
        await state.update_data(smart_gates=False)
        await state.clear()
        await callback.message.edit_text(text='Тут будет список подобранного оборудования.',
                                         reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')


# Хэндлер обрабатывающий ответ на количество ворот
@form_router.message(FSMEquipForm.smart_gates_count)
async def smart_gates_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        data = await state.get_data()
        pprint(data)
        await state.update_data(smart_gates_count=int(message.text))
        await state.clear()
        await message.answer(text='Тут будет список оборудования',
                             reply_markup=get_other_keyboard(cancel_keyboard))
    logger.info(f'Update handled by {start_form_equip.__name__}')