from math import inf
from valdec.decorators import validate
from validators import validate_float, validate_time_range
from typing import List


class Order:
    @validate
    def __init__(
            self,
            order_id: int,
            weight: float,
            region: int,
            delivery_hours: List[str]
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
