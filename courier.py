from useful_functions import validate_time_range, find_by
from pydantic import StrictStr, StrictInt
from valdec.decorators import validate
from statistics import mean
from typing import List
from order import Order
from time import time


class Courier:
    __capacity_on_transport = {'foot': 10, 'bike': 15, 'car': 50}
    __rate_on_transport = {'foot': 2, 'bike': 5, 'car': 9}

    def __get_type(self):
        return self.__type

    def __set_type(self, courier_type):

        # проверяем валидность транспортного средства
        if courier_type not in self.__capacity_on_transport.keys():
            raise ValueError(f'{courier_type} is not valid transport')

        # определяем грузоподъемность взависимости от транспорта
        temp = self.__capacity_on_transport[courier_type]

        # занято больше чем позволяет транспорт
        if self.__load_capacity - self.__free_load_capacity > temp:
            raise ValueError(
                f"Can not use this transport. Occupied currently: "
                f"{self.__load_capacity - self.__free_load_capacity}, but "
                f"transport `{courier_type}` allows only {temp}"
            )

        self.__type = courier_type

        self.__load_capacity = temp
        self.__free_load_capacity = self.__load_capacity

        # множитель заработка
        self.__earn_rate = self.__rate_on_transport[self.__type]

    courier_type = property(fget=__get_type, fset=__set_type)

    def __get_regions(self):
        return self.__regions

    def __set_regions(self, regions):
        self.__regions = regions

    regions = property(fget=__get_regions, fset=__set_regions)

    def __get_working_hours(self):
        return self.__working_hours

    def __set_working_hours(self, working_hours):
        # проверяем валидность рабочего графика
        for time_range in working_hours:
            validate_time_range(time_range)
        self.__working_hours = working_hours

    working_hours = property(fget=__get_working_hours, fset=__set_working_hours)

    def __get_free_load_capacity(self):
        return self.__free_load_capacity

    def __set_free_load_capacity(self, free_load_capacity):
        self.__free_load_capacity = free_load_capacity

    free_load_capacity = property(
        fget=__get_free_load_capacity, fset=__set_free_load_capacity
    )

    def __get_id(self):
        return self.__id

    def __set_id(self, courier_id):
        self.__id = courier_id

    id = property(fget=__get_id, fset=__set_id)

    @validate
    def __init__(
            self,  # strict types вызывают исключение и прекращают выполнение
            courier_id: StrictInt,
            courier_type: StrictStr,
            regions: List[StrictInt],
            working_hours: List[StrictStr]
    ):
        # активные заказы - массив словарей следующей структуры:
        #          'order' -> Обьект класса Order, сам заказ соот
        #          'accept time' -> время принятия заказа
        self.__active_orders = []  # ('order': Order, 'accept time': int)

        # Словарь значений `район - массив длительностей доставки`
        self.__regions_delivery_durations = {}  # region: delivery_durations

        self.__number_of_divorces = 0
        self.__earnings = 0
        self.__load_capacity = 0
        self.__free_load_capacity = 0

        self.id = courier_id
        self.courier_type = courier_type
        self.regions = regions
        self.working_hours = working_hours

    @validate
    def can_take(self, order: Order) -> bool:
        if order.delivery_hours not in self.__working_hours:
            return False  # не работает в эти часы

        if order.region not in self.__regions:
            return False  # не работает в этом регионе

        if self.__free_load_capacity - order.weight < 0:
            return False  # не может нести больше заказов

        return True

    @validate
    def complete_order(self, order_id: StrictInt):
        # находим заказ удовлетовряющий условию
        completed_order = find_by(
            self.__active_orders,
            lambda it: it['order'].id == order_id
        )

        # удаляем его из активных
        del self.__active_orders[completed_order]

        # освобождаем место у курьера
        self.free_load_capacity += completed_order['order'].weight

        # сохраняем длительность доставки
        delivery_duration = time() - completed_order['accept time']

        # если это не первая доставка у этого курьера в этом районе
        if completed_order['order'].region in self.__regions_delivery_durations:
            self.__regions_delivery_durations[
                completed_order['order'].region
            ].append(delivery_duration)  # добавляем длительность доставки
            # в массив длительностей доставки (для будущего просчета
            # среднего времени доставки)
        else:
            # если первая
            self.__regions_delivery_durations[
                completed_order.region['order']
            ] = [delivery_duration]  # создаем этот массив

        # перерасчитываем рейтинг и заработок

    def __accept_order(self, order: Order):
        if not self.can_take(order):
            raise ValueError('Can not accept this order')
        self.__active_orders.append({
            'order': order,
            'accept time': time()
        })
        self.free_load_capacity -= order.weight

    @validate
    def accept_orders(self, orders: List[Order]):
        for order in orders:
            self.__accept_order(order)
        self.__number_of_divorces += 1

    def __calculate_rating(self):
        td = []
        for durations in self.__regions_delivery_durations.values():
            td.append(mean(durations))  #
        t = min(td)
        rating = (60 * 60 - min(t, 60 * 60)) / (60 * 60) * 5
        self.__rating = rating

    def __calculate_earnings(self):
        self.__earnings = self.__number_of_divorces * 500 * self.__earn_rate
