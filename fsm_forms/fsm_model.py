from aiogram.fsm.state import State, StatesGroup

class FSMEquipForm(StatesGroup):
    name = State()  # Имя клиента
    type_home = State()  # Тип строения
    stage = State() # Стадия строительства
    wiring = State() # Проведена ли проводка
    one_button_switch = State() # Кол-во одноклавишных выключателей
    two_button_switch = State() # Кол-во двухклавишных выключателей
    cross_button = State() # Кол-во проходных выключателей
    group_lights = State() # Кол-во групп света
    led_strip = State() # Кол-во