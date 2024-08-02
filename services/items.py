"""В данном модуле описываются классы представляющие собой устройства Hite-Pro."""


class Items:
    """Базовый класс для объектов оборудования Hite-Pro."""
    def __init__(self, count: int, cost: int = 0):
        self.count = count
        self.cost = cost

    def summary(self):
        return self.cost * self.count

    def __add__(self, other):
        return self.__class__(self.count + other.count)


class Relay4m(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'Relay-4M'
        self.cost = 8380

    def __str__(self) -> str:
        descr = """Мастер-устройство модульной системы. 
        Блок радиореле используется для беспроводного управления 4-мя линиями электрической цепи
         и имеет шину данных для подключения ведомых устройств HiTE PRO Relay-S. 
         Получая сигнал от передатчиков блок замыкает/размыкает электрическую цепь. 
         Монтируется на DIN-рейку в распределительном щите."""
        return descr


class Relay4s(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'Relay-4S'
        self.cost = 7580

    def __str__(self) -> str:
        descr = """HiTE PRO Relay-4S – это четырехканальное реле является частью модульной системы,
         используется для беспроводного управления 4-мя линиями электрической цепи 
         и имеет шину данных для подключения к радиопередающему устройству (HiTE PRO Relay-M).
        Получая сигнал от передатчиков блок замыкает/размыкает электрическую цепь. 
        Передатчиками являются другие устройства HiTE PRO: беспроводные выключатели,
         пульты ДУ, датчики, сервер умного дома."""
        return descr


class RelayLed3S(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'Relay-LED3S'
        self.cost = 7580

    def __str__(self) -> str:
        descr = """HiTE PRO Relay-LED3S – это трехканальное реле является частью модульной системы,
         используется для беспроводного управления 3-мя линиями электрической цепи (светодиодными или RGB-лентами)
          и имеет шину данных для подключения к радиопередающему устройству (HiTE PRO Relay-M).
           Получая сигнал от передатчиков блок замыкает/размыкает электрическую цепь. 
           Передатчиками являются другие устройства HiTE PRO: беспроводные выключатели,
            пульты ДУ, датчики, сервер умного дома."""
        return descr


class Relay1(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'Relay-1'
        self.cost = 2780

    def __str__(self) -> str:
        descr = """Компактный одноканальный блок радиореле Relay-1 подключается к светильнику или другому электроприбору,
         которым нужно управлять с помощью передатчиков или сервера умного дома HiTE PRO.
          Получая от них сигнал блок Relay-1 замыкает/размыкает электрическую цепь."""
        return descr


class Relay2(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'Relay-2'
        self.cost = 4180

    def __str__(self) -> str:
        descr = """Компактный двухканальный блок радиореле Relay-2 подключается к светильнику или другому электроприбору,
         которым нужно управлять с помощью передатчиков или сервера умного дома HiTE PRO.
        Получая от них сигнал блок Relay-2 замыкает/размыкает электрическую цепь."""
        return descr


class RelayF1(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'Relay-F1'
        self.cost = 3180

    def __str__(self) -> str:
        descr = """Компактный одноканальный блок радиореле Relay-F1 подключается в разрыв фазы к существующему обычному 
        выключателю и позволяет добавить к нему беспроводное управление.
         Функционал существующего обычного выключателя можно сохранить благодаря двум специальным выходам в блоке.
        Блок замыкает/размыкает электрическую цепь при получении сигнала от передатчиков, с которыми связан."""
        return descr


class RelayF2(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'Relay-F2'
        self.cost = 4580

    def __str__(self) -> str:
        descr = """Компактный двухканальный блок радиореле Relay-F2 подключается в разрыв фазы к существующему обычному
         выключателю и позволяет добавить к нему беспроводное управление.
          Функционал существующего обычного выключателя можно сохранить благодаря двум специальным выходам в блоке."""
        return descr


class Relay16A(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'Relay-16A'
        self.cost = 3180

    def __str__(self) -> str:
        descr = """Компактный одноканальный блок приема сигнала с функцией диммирования (регулировки яркости света)
         для светодиодных ламп и лент.
        Получая сигнал от передатчиков HiTE PRO блок замыкает/размыкает/диммирует электрическую цепь."""
        return descr


class RelayLed(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'Relay-LED'
        self.cost = 3180

    def __str__(self) -> str:
        descr = """Компактный одноканальный блок приема сигнала с функцией диммирования (регулировки яркости света)
         для светодиодных ламп и лент.
          Получая сигнал от передатчиков HiTE PRO блок замыкает/размыкает/диммирует электрическую цепь."""
        return descr


class RelayDim(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'Relay-DIM'
        self.cost = 3180

    def __str__(self) -> str:
        descr = """Используется для диммирования (регулировки яркости света)."""
        return descr


class RelayDrive(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'Relay-Drive'
        self.cost = 3180

    def __str__(self) -> str:
        descr = """HiTE PRO Relay-DRIVE используется для беспроводного управления электроприводами 
        (электрошторы/жалюзи, рольставни, ворота и т.д.)  сетевого напряжения ~220В с концевыми выключателями.

        Подключается «в разрыв» цепи питания перед электроприводом, которым нужно управлять с помощью беспроводных
         выключателей или ДУ пультов HiTE PRO.
        Замыкает/размыкает цепь питания при получении сигнала от передатчиков, с которыми связан."""
        return descr


class RelayRGBW(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'Relay-RGBW'
        self.cost = 3180

    def __str__(self) -> str:
        descr = """Компактный одноканальный блок приема сигнала с функцией диммирования — регулировки яркости света,
         а также смены цвета и управления цветовой температурой для RGB и RGBW светодиодных лент.
          Получая сигнал от передатчиков HiTE PRO блок замыкает/размыкает электрическую цепь и диммирует/меняет цвет."""
        return descr


class SmartMotion(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'Smart Motion'
        self.cost = 2840

    def __str__(self) -> str:
        descr = """Позволяет получить информацию об уровне освещенности и любых движениях людей в помещении."""
        return descr


class SmartAIR(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'Smart Air'
        self.cost = 2840

    def __str__(self) -> str:
        descr = """Предоставляет информацию о температуре и влажности помещения в приложении HiTE PRO.
        Отправляет радиосигнал на Включение / Выключение блоку приема при изменении температуры или влажности."""
        return descr


class SmartWater(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'Smart Water'
        self.cost = 2840

    def __str__(self) -> str:
        descr = """Предоставляет информацию о температуре и влажности помещения в приложении HiTE PRO.
        Отправляет радиосигнал на Включение / Выключение блоку приема при изменении температуры или влажности."""
        return descr


class UNI(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'UNI'
        self.cost = 1740

    def __str__(self) -> str:
        descr = """Трехканальный радиомодуль UNI подключается к обычному одноклавишному,
         двухклавишному или трехклавишному выключателю. В результате такой выключатель становится беспроводным,
          т.е. способным передавать управляющий сигнал на любой из блоков управления."""
        return descr


class LE1(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'Радиовыключатель LE-1'
        self.cost = 1380

    def __str__(self) -> str:
        descr = """Кнопочный одноканальный беспроводной выключатель с рамкой серии Legrand Etika.
         Работает от одной батарейки более 7 лет. Частота 868 МГц, на которой работает выключатель,
          позволяет управлять освещением на расстоянии до 250 м. 
          Имеет квадратную кнопку и представлен в двух цветах: белый и слоновая кость."""
        return descr


class LE2(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'Радиовыключатель LE-2'
        self.cost = 1680

    def __str__(self) -> str:
        descr = """Кнопочный двухканальный беспроводной выключатель с рамкой серии Legrand Etika. 
        Работает от одной батарейки более 7 лет. Частота 868 МГц, на которой работает выключатель, 
        позволяет управлять освещением на расстоянии до 250 м. 
        Имеет квадратную кнопку и представлен в двух цветах: белый и слоновая кость."""
        return descr


class Gateway(Items):
    def __init__(self, count=1) -> None:
        super().__init__(count)
        self.name = 'Радиовыключатель LE-2'
        self.cost = 8380

    def __str__(self) -> str:
        descr = """Сервер умного дома используется для беспроводного управления освещением и электроприборами через
         приложение HiTE PRO для умного дома или голосовых помощников Алиса, Siri, Маруся или Google Assistant."""
        return descr


