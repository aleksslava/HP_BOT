'''Кнопки для inline клавиатуры'''
LEXICON_INLINE_RU: dict[str, str | dict[str, str]] = {
    'start': {'descr': 'Запуск бота',
              'callback': 'start'},
    'help': {'descr': 'Помощь',
             'callback': 'help'},
    'equip': {'descr': 'Устройства',
              'callback': 'equip'},
    'standart': {'standart': 'Типовой расчёт',
                 'callback': 'standart'},
    'items': {'descr': 'Устройства Hite-Pro',
              'callback': 'items'}
}


# Клавиатура для главного меню бота
LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Старт бота',
    '/equip': 'Подобрать оборудование',
    '/standart': 'Типовые проекты умного дома ',
    '/items': 'Оборудование Hite-Pro!',
    '/help': 'Помощь'
}

LEXICON_RU: dict[str, str] = {
    'start': 'Выберите необходимый пункт меню',
    'help': 'Тут будет описание возможностей бота и каждого отдельного пункта меню',
    'equip': '',
    'standart': '',
    'items': ''
}