from _dataclasses import CourierDataClass
from useful_functions import validate_time_range, find_by
from pydantic import StrictStr, StrictInt
from valdec.decorators import validate
from daterange import DateRange
from statistics import mean
from typing import List, Dict, Any
from order import Order
from time import time


class Courier(CourierDataClass):
    @validate
    def can_take(self, order: Order) -> bool:
        work_in_this_time = True
        for working_time in self.working_hours:
            for delivery_time in order.delivery_hours:
                work_in_this_time = work_in_this_time and \
                                    delivery_time not in working_time
        if not work_in_this_time:
            # не работает в это время
            return False

        if order.region not in self.__regions:
            return False  # не работает в этом регионе

        if self.__free_load_capacity - order.weight < 0:
            return False  # не может нести больше заказов

        return True

    @validate
    def complete_order(self, order_id: StrictInt):
        # # -------------------------
        # # Fix due to new conditions
        # # -------------------------
        # находим заказ удовлетовряющий условию
        completed_order_index = find_by(
            self.__active_orders,
            lambda it: it['order'].id == order_id
        )
        completed_order = self.__active_orders[completed_order_index]

        # удаляем его из активных
        del self.__active_orders[completed_order_index]

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
                completed_order['order'].region
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

    def to_dict(self):
        return {
            "courier_id": self.id,
            "courier_type": self.courier_type,
            "region": self.regions,
            "working_hours": [str(working_hours) for working_hours in
                              self.working_hours]
        }
