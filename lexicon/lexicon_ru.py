# Кнопки для inline клавиатуры"""
LEXICON_MAIN_INLINE_RU: dict[str, str] = {
    'Подбор оборудования': 'equip',
    'Типовые проекты умного дома': 'standart',
    'Устройства Hite-Pro': 'items',
    'Помощь': 'help',
}


# Клавиатура для главного меню бота
LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Старт бота',
    '/equip': 'Подобрать оборудование',
    '/standart': 'Типовые проекты умного дома ',
    '/items': 'Оборудование Hite-Pro!',
    '/help': 'Помощь'
}
# Клавиатура для шага - выбор типа строения
HOME_TYPES: dict[str, str] = {
    'Квартира': 'apartment',
    'Частный дом': 'cottage',
    'Офис': 'office',
    'Другое строение': 'another_structure',
}
# Этапы постройки
REPAIR_STAGE: dict[str, str] = {
    'Планирую ремонт': 'plane',
    'На этапе ремонта': 'repair',
    'Ремонт завершен': 'repair_complete'
}
# Общий словарь
LEXICON_RU: dict[str, str] = {
    'start': 'Выберите необходимый пункт меню',
    'help': 'Тут будет описание возможностей бота и каждого отдельного пункта меню',
    'name': 'Введите своё имя!',
    'name_false': 'Вы ввели некорректное имя. Имя не должно содержать цифр.\n Попробуйте ещё раз.',
    'type_home': 'Выберите тип строения в котором планируется установка умного дома!',
    'stage': 'Выберите на каком этапе вы сейчас находитесь',
    'wiring': 'Проводка до выключателей уже проведена?',
    'one_button_count': 'Напишите цифрами количество одноклавишных выключателей',
    'two_button_count': 'Напишите цифрами количество двухклавишных выключателей',
    'cross_button_existence': 'Есть ли у Вас проходные и перекрёстные выключатели?',
    'cross_button_one': 'Напишите цифрами количество проходных однокалвишных выключателей',
    'cross_button_two': 'Напишите цифрами количество проходных двухклавишных выключателей',
    'smart_socket_existence': 'Нужно ли сделать какие-то из розеток умными?',
    'button_count_false': 'Неверный формат данных.\n Убедитесь, что вы ввели количество цифрами.\n Попробуйте ещё раз!',
    'cross_button_count_false': 'Количество проходных выключателей должно быть кратным 2.\n Попробуйте ещё раз!',
    'cross_switch_one': 'Напишите количество перекрёстных одноклавишных выключателей',
    'cross_switch_two': 'Напишите количество перекрёстных двухклавишных выключателей',
    'group_lights': 'Напишите цифрами планируемое количество групп света',
    'led_strips_existence': 'Будут ли использоваться светодиодные ленты?',
    'led_strips_count': 'Введите количество одноцветных светодиодных лент',
    'repeat': 'Вы уже находитесь в этом пункте меню.',
    'cancel': 'Вы отменили прохождение анкеты. Возврат в главное меню.'
}
# Кнопки отмены
cancel_keyboard: dict[str, str] = {
    'Отменить прохождение анкеты': 'cancel'
}

# Кнопки да \ нет
yes_no_keyboard: dict[str, str] = {
    'Да': 'yes',
    'Нет': 'no'
}