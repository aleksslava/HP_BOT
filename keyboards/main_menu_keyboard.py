from lexicon.lexicon_ru import LEXICON_COMMANDS
from aiogram import Bot
from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup


# Главное меню бота
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in LEXICON_COMMANDS.items()
    ]

    await bot.set_my_commands(main_menu_commands)


# Главная инлайн клавиатура бота
def inline_main_menu(args: dict[str, str]):
    buttons: list = []
    for text, callback in args.items():
        buttons.append([InlineKeyboardButton(
            text=text,
            callback_data=callback
        )])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

