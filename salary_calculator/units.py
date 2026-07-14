from enum import Enum


class InputUnit(str, Enum):
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"


HOURS_PER_UNIT = {
    InputUnit.MINUTE: 1 / 60,
    InputUnit.HOUR: 1,
    InputUnit.DAY: 8,
    InputUnit.WEEK: 40,
    InputUnit.MONTH: 173.6667,
    InputUnit.YEAR: 2084,
}


def normalize_to_hour(amount: float, unit: InputUnit) -> float:
    return amount / HOURS_PER_UNIT[unit]


def from_hour(hourly_rate: float) -> dict[str, float]:
    return {
        unit.value: hourly_rate * hours
        for unit, hours in HOURS_PER_UNIT.items()
    }
