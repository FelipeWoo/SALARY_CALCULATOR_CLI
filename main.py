import requests
from enum import Enum

# === CURRENCIES ===
CURRENCY_CODES = [
    "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN",
    "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BOV",
    "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHE", "CHF",
    "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CUC", "CUP", "CVE",
    "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD",
    "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD",
    "HNL", "HRK", "HTG", "HUF", "IDR", "ILS", "INR", "IQD", "IRR", "ISK",
    "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD",
    "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL",
    "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN",
    "MXV", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR",
    "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD",
    "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLL",
    "SOS", "SRD", "SSP", "STN", "SVC", "SYP", "SZL", "THB", "TJS", "TMT",
    "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "USN",
    "UYI", "UYU", "UYW", "UZS", "VED", "VES", "VND", "VUV", "WST", "XAF",
    "XAG", "XAU", "XBA", "XBB", "XBC", "XBD", "XCD", "XDR", "XOF", "XPD",
    "XPF", "XPT", "XSU", "XTS", "XUA", "XXX", "YER", "ZAR", "ZMW", "ZWL"
]
Currency = Enum("Currency", {code: code for code in CURRENCY_CODES})

# === UNITS: hours contained in each unit ===
HOURS_PER_UNIT = {
    "MINUTE": 1 / 60,
    "HOUR": 1,
    "DAY": 8,
    "WEEK": 40,
    "MONTH": 173.67,   # 21.67 (average workdays per month 260/12) × 8
    "YEAR": 2084       # 260 workdays × 8
}

InputUnit = Enum("InputUnit", {k: k for k in HOURS_PER_UNIT.keys()})

# === Normalizer ===
def normalize_to_hour(amount: float, unit: InputUnit) -> float:
    return amount / HOURS_PER_UNIT[unit.name]

def from_hour(hourly_rate: float) -> dict:
    return {k: hourly_rate * v for k, v in HOURS_PER_UNIT.items()}

# === CURRENCY CONVERTER ===
class Salary:
    def __init__(self, from_currency: Currency, to_currency: Currency):
        self.from_currency = from_currency.value
        self.to_currency = to_currency.value
        self.exchange_rate = None

    def convert(self, amount: float) -> float | None:
        url = f"https://api.frankfurter.app/latest?amount={amount}&from={self.from_currency}&to={self.to_currency}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            result = data["rates"][self.to_currency]
            self.exchange_rate = result / amount
            return result
        return None

# === UTILITIES ===
def display_salary(title: str, breakdown: dict, currency: str):
    print(f"\n{title}")
    for k, v in breakdown.items():
        print(f"{k.capitalize():<10}: {v:,.2f} {currency}")

def input_enum(prompt: str, enum_cls: Enum):
    while True:
        value = input(prompt).upper()
        try:
            return enum_cls[value]
        except KeyError:
            print("*" * 60)
            print(f"{value} is not valid. Options: {list(enum_cls.__members__)}")
            print("*" * 60)

# === MAIN ===
def main():
    print("-" * 60)
    print("Welcome to the salary calculation system with conversions")
    print("-" * 60)

    amount = float(input("Enter salary amount: "))
    salary_type = input_enum("Payment type [minute, hour, day, ...]: ", InputUnit)
    original_currency = input_enum("Source currency (e.g. USD): ", Currency)
    target_currency = input_enum("Target currency (e.g. MXN): ", Currency)

    hourly_rate = normalize_to_hour(amount, salary_type)
    salary_converter = Salary(original_currency, target_currency)
    converted_hourly_rate = salary_converter.convert(hourly_rate)

    if converted_hourly_rate is None:
        print("Conversion error.")
        return

    original = from_hour(hourly_rate)
    converted = from_hour(converted_hourly_rate)

    print("-" * 60)
    print(f"Exchange rate: 1 {original_currency.value} = {salary_converter.exchange_rate:.2f} {target_currency.value}")
    print("-" * 60)
    display_salary(f"Original salary in {original_currency.value}", original, original_currency.value)
    print("-" * 60)
    display_salary(f"Converted salary in {target_currency.value}", converted, target_currency.value)
    print("-" * 60)

if __name__ == "__main__":
    main()
