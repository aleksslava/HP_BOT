from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Билдер клавиатуры, на вход принимаются словари с кнопками (Название кнопки, callback), width - кол-во кнопок в ряду
def get_other_keyboard(*args: dict[str, str], width=2) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for dct in args:
        kb_builder.row(*[InlineKeyboardButton(
            callback_data=callback,
            text=text
        ) for text, callback in dct.items()],
                       width=width)
    return kb_builder.as_markup()

