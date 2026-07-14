from enum import Enum
from typing import TypeVar

from salary_calculator.converter import SalaryConverter
from salary_calculator.currencies import Currency
from salary_calculator.units import InputUnit, from_hour, normalize_to_hour

EnumType = TypeVar("EnumType", bound=Enum)


def display_salary(title: str, breakdown: dict[str, float], currency: str) -> None:
    print(f"\n{title}")
    for unit, value in breakdown.items():
        print(f"{unit.capitalize():<10}: {value:,.2f} {currency}")


def input_enum(prompt: str, enum_cls: type[EnumType]) -> EnumType:
    while True:
        value = input(prompt).upper()
        try:
            return enum_cls[value]
        except KeyError:
            print("*" * 60)
            print(f"{value} is not valid. Options: {list(enum_cls.__members__)}")
            print("*" * 60)


def main() -> None:
    print("-" * 60)
    print("Welcome to the salary calculation system with conversions")
    print("-" * 60)

    amount = float(input("Enter salary amount: "))
    salary_type = input_enum("Payment type [minute, hour, day, month, year]: ", InputUnit)
    original_currency = input_enum("Source currency (e.g. USD): ", Currency)
    target_currency = input_enum("Target currency (e.g. MXN): ", Currency)

    hourly_rate = normalize_to_hour(amount, salary_type)
    converter = SalaryConverter(original_currency, target_currency)
    converted_hourly_rate = converter.convert(hourly_rate)

    if converted_hourly_rate is None or converter.exchange_rate is None:
        print("Conversion error.")
        return

    original = from_hour(hourly_rate)
    converted = from_hour(converted_hourly_rate)

    print("-" * 60)
    print(
        f"Exchange rate: 1 {original_currency.value} = "
        f"{converter.exchange_rate:.2f} {target_currency.value}"
    )
    print("-" * 60)
    display_salary(
        f"Original salary in {original_currency.value}",
        original,
        original_currency.value,
    )
    print("-" * 60)
    display_salary(
        f"Converted salary in {target_currency.value}",
        converted,
        target_currency.value,
    )
    print("-" * 60)
