from services.items import *

"""В данном модуле описывается класс принимающий словарь с ответами пользователя
при прохождении анкеты и возвращающий необходимый комплект устройств."""


class ReplyUser:
    def __init__(self, reply_dct: dict[str, str | int | bool]) -> None:
        self.items = reply_dct

        self.result_obj = []

    # Функция принимает количество групп света, розеток и лед лент и рассчитывает количество блоков на дин рейку.
    def get_blocks_din(self,
                       lights: int,
                       sockets: int,
                       led: int,
                       rgb: int) -> None:

        led_lights_block = RelayLed3S(rgb) + RelayLed3S(
            led // 3 if led % 3 else led // 3 + 1)  # Количество блоков relay-led3
        count_power = lights + sockets  # Количество потребителей
        block_ms_count = count_power // 4 if count_power % 4 else count_power // 4 + 1  # Количество блоков relay-4ms
        all_blocks = led_lights_block.count + block_ms_count
        relay_4m = Relay4m(all_blocks // 6 * 2) if all_blocks // 6 else Relay4m((all_blocks // 6 + 1) * 2)
        relay_4s = Relay4s(all_blocks - relay_4m.count)

        for item in (relay_4m, relay_4s, led_lights_block):
            self.result_obj.append(item)

    # Функция принимает количество выключателей и расчитывает количество компактных блоков.
    def get_compact_blocks(self,
                           one_button_switch: int,
                           two_button_switch: int,
                           cross_button_one: int,
                           cross_button_two: int,
                           cross_switch_one: int,
                           cross_switch_two: int,
                           ) -> None:

        relay_f1 = RelayF1(one_button_switch + cross_button_one // 2)
        relay_f2 = RelayF2(two_button_switch + cross_button_two // 2)
        uni = UNI((cross_button_one + cross_button_two) // 2 +
                  cross_switch_one + cross_switch_two)

        for item in (relay_f1, relay_f2, uni):
            self.result_obj.append(item)

    # Функция принимающая количество умных розеток и возыращающая количество компактных реле.
    def smart_socket_compact(self, socket) -> None:
        self.result_obj.append(Relay16A(socket))

    def get_block_electric_warm(self, count: int) -> None:
        self.result_obj.append(Relay16A(count))


a = {'cross_button_existence': True,
     'cross_button_one_count': 2,
     'cross_button_two_count': 4,
     'cross_switch_one_count': 6,
     'cross_switch_two_count': 3,
     'home_type': 'cottage',
     'name': 'slava',
     'one_button_switch': 5,
     'smart_cornice_count': 3,
     'smart_cornice_existence': True,
     'smart_gates': True,
     'smart_socket_count': 3,
     'smart_socket_existence': True,
     'stage': 'plane',
     'two_button_count': 5,
     'warm_floor_electric': True,
     'warm_floor_electric_count': 4,
     'warm_floor_water': True,
     'warm_floor_water_count': 2,
     'water_protect_existence': True,
     'water_rizer_count': 6,
     'wet_zone_count': 5,
     'wiring': 'yes'}
