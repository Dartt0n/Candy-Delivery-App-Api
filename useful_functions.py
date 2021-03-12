from math import inf
from valdec.decorators import validate
from regex import match
from typing import List, Callable, Iterable


def find_by(arr: Iterable, condition: Callable) -> int:
    for element, index in enumerate(arr):
        if condition(element):
            return index
    raise ValueError('No such element in iterable object')


@validate
def validate_time_range(time_range: str):
    assert match(
        "([0-1]?[0-9]|2[0-3]):[0-5][0-9]-([0-1]?[0-9]|2[0-3]):[0-5][0-9]",
        time_range
    )


@validate
def validate_float(
        number: float,
        accuracy: int,
        min_value: float = 0,
        max_value: float = inf,
):
    assert number == round(number, accuracy)
    assert number <= max_value
    assert number >= min_value
