from collections import Iterable
from datetime import datetime, timedelta
from typing import Iterator, Union
from pydantic import StrictStr
from valdec.decorators import validate
from useful_functions import validate_time_range


class DateRange:
    @validate
    def __init__(self, time_range: StrictStr):
        validate_time_range(time_range)

        self.start, self.end = time_range.split('-')

        self.start = datetime.strptime(self.start, '%H:%M')
        self.end = datetime.strptime(self.end, '%H:%M')

        if self.end <= self.start:
            raise ValueError(f"Wrong time range: {time_range}")

    def __str__(self) -> str:
        return f'{self.start.strftime("%H:%M")}-{self.end.strftime("%H:%M")}'

    def __contains__(self, time_range):
        if isinstance(time_range, str):
            # переводим ошибку в строку
            if '-' not in time_range:  # одно значение, а не промежуток
                time_range = DateRange(time_range+'-'+time_range)
            else:
                time_range = DateRange(time_range)
        elif not isinstance(time_range, DateRange):
            # неподдерживаемый тип
            raise TypeError(f'{time_range} is not Str or DateRange')

        return time_range.start >= self.start and time_range.end <= self.end
