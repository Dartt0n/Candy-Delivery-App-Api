from typing import List
from valdec.decorators import validate
from validators import validate_time_range
from pydantic import StrictStr


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
