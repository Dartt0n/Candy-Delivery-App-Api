from useful_functions import validate_time_range, find_by
from valdec.decorators import validate
from pydantic import StrictStr
from typing import List
from order import Order


class Courier:
    __capacity_on_transport = {'foot': 10, 'bike': 15, 'car': 50}

    @validate
    def __init__(
            self,
            courier_id: int,
            courier_type: StrictStr,
            regions: List[int],
            working_hours: List[StrictStr]
    ):
        self.__id = courier_id

        # проверяем валидность транспортного средства
        if courier_type not in self.__capacity_on_transport.keys():
            raise ValueError(f'{courier_type} is not valid transport')
        self.__type = courier_type

        self.__regions = regions

        # проверяем валидность рабочего графика
        for time_range in working_hours:
            validate_time_range(time_range)

        self.__working_hours = working_hours

        # определяем грузоподъемность взависимости от транспорта
        self.__load_capacity = self.__capacity_on_transport[self.__type]
        self.__free_load_capacity = self.__load_capacity

        self.__active_orders = []

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
        # todo other calculations
