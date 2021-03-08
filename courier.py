from useful_functions import validate_time_range, find_by
from valdec.decorators import validate
from pydantic import StrictStr, StrictInt
from typing import List
from order import Order


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

    free_load_capacity = property(fget=__get_free_load_capacity,
                                  fset=__set_free_load_capacity)

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
        self.__active_orders = []
        self.earnings = 0
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
    def complete_order(self, order_id: int):
        # находим заказ удовлетовряющий условию
        x = find_by(self.__active_orders, lambda it: it.id == order_id)
        # удаляем его из активных
        self.__active_orders.remove(x)
        # выполняем дополнительные вычисления
        self.free_load_capacity += x.weight
        # todo handle completed order
