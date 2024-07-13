from aiogram import Router, F
from fsm_forms.fsm_model import FSMEquipForm
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

form_router = Router()


@form_router.message(Command(commands='equip'))
async def start_form_equip(message: Message, state: FSMContext):
    await state.set_state(FSMEquipForm.name)
    await message.answer(text='Введите своё имя')

