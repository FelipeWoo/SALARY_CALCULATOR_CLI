import requests

from salary_calculator.currencies import Currency

API_URL = "https://api.frankfurter.app/latest"
REQUEST_TIMEOUT_SECONDS = 10


class SalaryConverter:
    def __init__(self, from_currency: Currency, to_currency: Currency):
        self.from_currency = from_currency.value
        self.to_currency = to_currency.value
        self.exchange_rate: float | None = None

    def convert(self, amount: float) -> float | None:
        if self.from_currency == self.to_currency:
            self.exchange_rate = 1.0
            return amount

        params = {
            "from": self.from_currency,
            "to": self.to_currency,
        }

        try:
            response = requests.get(
                API_URL,
                params=params,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            exchange_rate = float(response.json()["rates"][self.to_currency])
        except (requests.RequestException, KeyError, TypeError, ValueError):
            return None

        self.exchange_rate = exchange_rate
        return amount * exchange_rate
