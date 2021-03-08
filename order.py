from math import inf
from valdec.decorators import validate
from useful_functions import validate_float, validate_time_range


class Order:
    @validate
    def __init__(
            self,
            order_id: int,
            weight: float,
            region: int,
            delivery_hours: list[str]
    ):
        self.__id = order_id

        # проверяем валидность веса
        validate_float(weight, accuracy=2, min_value=0.01, max_value=50)
        self.__weight = weight

        self.__region = region

        # проверяем валидность часов доставки
        for time_range in delivery_hours:
            validate_time_range(time_range)
        self.__delivery_hours = delivery_hours

    def __get_delivery_hours(self): return self.__delivery_hours

    delivery_hours = property(__get_delivery_hours)

    def __get_region(self): return self.__region

    region = property(__get_region)

    def __get_weight(self): return self.__weight

    weight = property(__get_weight)

    def __get_id(self): return self.__id

    id = property(__get_id)
