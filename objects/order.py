from misc.useful_functions import validate_float, validate_time_range
from pydantic.types import StrictInt, StrictFloat, StrictStr
from valdec.decorators import validate
from typing import Union


class Order:
    def __get_delivery_hours(self):
        return self.__delivery_hours

    def __set_delivery_hours(self, delivery_hours):
        # проверяем валидность часов доставки
        for time_range in delivery_hours:
            validate_time_range(time_range)
        self.__delivery_hours = delivery_hours

    delivery_hours = property(fget=__get_delivery_hours, fset=__set_delivery_hours)

    def __get_region(self):
        return self.__region

    def __set_region(self, region):
        self.__region = region

    region = property(fget=__get_region, fset=__set_region)

    def __get_weight(self):
        return self.__weight

    def __set_weight(self, weight):
        # проверяем валидность веса
        validate_float(weight, accuracy=2, min_value=0.01, max_value=50)
        self.__weight = weight

    weight = property(fget=__get_weight, fset=__set_weight)

    def __get_id(self):
        return self.__id

    def __set_id(self, order_id):
        self.__id = order_id

    id = property(fget=__get_id, fset=__set_id)

    @validate
    def __init__(
        self,
        order_id: StrictInt,
        weight: Union[StrictFloat, StrictInt],
        region: StrictInt,
        delivery_hours: list[StrictStr],
        **additional_data
    ):
        self.id = order_id
        self.weight = weight
        self.region = region
        self.delivery_hours = delivery_hours
        self.config = additional_data
