from aiogram.fsm.state import State, StatesGroup

'''Анкета для опроса клиента и подбора оборудования'''
class FSMEquipForm(StatesGroup):
    name = State()  # Имя клиента
    type_home = State()  # Тип строения
    stage = State()  # Стадия строительства
    wiring = State()  # Проведена ли проводка?
    one_button_switch = State()  # Кол-во одноклавишных выключателей
    two_button_switch = State()  # Кол-во двухклавишных выключателей
    cross_button = State()  # Кол-во проходных выключателей
    group_lights = State()  # Кол-во групп света
    led_strips = State()  # Будут ли лед ленты?
    led_strips_count = State()  # Кол-во лед лент одноцветных
    rgb_strips_count = State()  # Кол-во rgb  лент
    rgbw_strips_count = State()  # Кол-во rgbw лент
    dim_lights = State()  # Будут диммируемые группы света?
    dim_lights_count = State()  # Кол-во диммируемых групп света
    smart_socket = State()  # Будут умные розетки?
    smart_socket_count = State()  # Кол-во умных розеток.
    water_protect = State()  # Нужна защита от протечек?
    wet_zone_count = State()  # Кол-во мокрых зон
    water_rizer_count = State()  # Количество стояков системы водоснабжения
    smart_cornice = State()  # Будут электрокарнизы?
    smart_cornice_count = State()  # Количество карнизов
    warm_floor = State()  # Будет тёплый пол?
    warm_floor_type = State()  # Тип тёплого пола
    warm_floor_count = State()  # Количество зон тёплого пола
    smart_gates = State()  # Будут откатные ворота?
    smart_gates_count = State()  # Кол-во ворот откатных.


'''Анкета для опроса клиента перед отправкой типового предложения'''
class FSM_standart_Form(StatesGroup):
    name = State()  # Имя клиента
    stage = State()  # Стадия стоительства
