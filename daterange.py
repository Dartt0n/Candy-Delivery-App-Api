from collections import Iterable
from datetime import datetime, timedelta
from typing import Iterator, Union
from pydantic import StrictStr
from valdec.decorators import validate
from validators import validate_time_range


class DateRange(Iterable):
    @validate
    def __init__(self, time_range: StrictStr):
        validate_time_range(time_range)

        self.start, self.end = time_range.split('-')

        self.start = datetime.strptime(self.start, '%H:%M')
        self.end = datetime.strptime(self.end, '%H:%M') + timedelta(minutes=1)

    def __iter__(self) -> Iterator:
        return self

    def __next__(self):
        self.start += timedelta(minutes=1)
        if self.start == self.end:
            raise StopIteration
        return self.start.strftime("%H:%M")

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
