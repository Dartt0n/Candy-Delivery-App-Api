import re
from pydantic.types import StrictInt, StrictStr
from valdec.decorators import validate
from typing import List, Dict, Any, Union
from misc.daterange import DateRange


class Courier:
    __capacity_on_transport = {"foot": 10, "bike": 15, "car": 50}
    __rate_on_transport = {"foot": 2, "bike": 5, "car": 9}

    def __get_type(self):
        return self.__type

    def __set_type(self, courier_type):

        # проверяем валидность транспортного средства
        if courier_type not in self.__capacity_on_transport.keys():
            raise ValueError(f"{courier_type} is not valid transport")

        # определяем грузоподъемность взависимости от транспорта
        temp = self.__capacity_on_transport[courier_type]

        # занято больше чем позволяет транспорт
        if self.__workload > temp:
            raise ValueError(
                f"Can not use this transport. Occupied currently: "
                f"{self.__workload}, but "
                f"transport `{courier_type}` allows only {temp}"
            )

        self.__type = courier_type

        self.__load_capacity = temp

        # множитель заработка
        self.__earn_rate = self.__rate_on_transport[self.__type]

    def __get_earn_rate(self):
        return self.__earn_rate

    earn_rate = property(fget=__get_earn_rate)

    courier_type = property(fget=__get_type, fset=__set_type)

    def __get_regions(self):
        return self.__regions

    def __set_regions(self, regions):
        rg = []
        for region in regions:
            if not isinstance(region, int) or region <= 0:
                raise ValueError
            rg.append(region)
        self.__regions = rg

    regions = property(fget=__get_regions, fset=__set_regions)

    def __get_working_hours(self):
        return [str(wh) for wh in self.__working_hours]

    def __set_working_hours(self, working_hours):
        self.__working_hours = []
        for time_range in working_hours:
            self.__working_hours.append(DateRange(time_range))

    working_hours = property(fget=__get_working_hours, fset=__set_working_hours)

    def __get_id(self):
        return self.__id

    def __set_id(self, courier_id):
        self.__id = courier_id

    id = property(fget=__get_id, fset=__set_id)

    def __get_free_load_capacity(self):
        return self.__load_capacity - self.__workload

    free_load_capacity = property(fget=__get_free_load_capacity)

    @validate
    def __init__(
        self,  # strict types вызывают исключение и прекращают выполнение
        courier_id: StrictInt,
        courier_type: StrictStr,
        regions: List[StrictInt],
        working_hours: List[StrictStr],
        number_of_divorces: StrictInt = 0,
        earnings: Union[int, float] = 0,
        workload: Union[int, float] = 0,
    ):
        self.number_of_divorces = number_of_divorces
        self.earnings = earnings
        self.__workload = workload

        self.id = courier_id
        self.courier_type = courier_type
        self.regions = regions
        self.working_hours = working_hours

    @validate
    def config(self, data: Dict):
        key, value = list(data.items())[0]
        if key == "courier_type":
            self.courier_type = value
        elif key == "working_hours":
            self.working_hours = value
        elif key == "regions":
            self.regions = value
        else:
            raise ValueError("Wrong config parameter")

    def can_take(self, order) -> bool:
        hours_flag = False
        for wh in self.working_hours:
            wh = DateRange(wh)
            for dh in order.delivery_hours:
                dh = DateRange(dh)
                hours_flag = hours_flag or dh in wh  # работает ли в часы доставки

        region_flag = False
        for r in self.regions:
            region_flag = region_flag or r == order.region  # работает ли в этом регионе
        weight_flag = order.weight <= self.free_load_capacity  # может нести груз

        return hours_flag and region_flag and weight_flag
