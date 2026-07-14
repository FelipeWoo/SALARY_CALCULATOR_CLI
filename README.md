# Salary Calculator CLI

A Python command-line application that normalizes salaries across time units and converts them between currencies using current exchange rates from the [Frankfurter API](https://www.frankfurter.app/).

## Objective

Accurately calculate the number of working hours in a year using average values based on standard workweeks. This document serves as a foundation for converting salaries between different time units (minute, hour, day, week, month, year), and to demonstrate API integration via the command line (CLI).

---

## Technical Overview: Currency Conversion via API

This project demonstrates how to **connect to an external API** using Python through the command line interface (CLI), and fetch **real-time exchange rates**.

### API Used

* **Endpoint**: `https://api.frankfurter.app/latest`
* **Parameters**:

  * `amount`: the numeric value to convert
  * `from`: source currency code (e.g., USD)
  * `to`: target currency code (e.g., MXN)

### Example Request

```bash
curl "https://api.frankfurter.app/latest?amount=100&from=USD&to=MXN"
```

### JSON Response (Example)

```json
{
  "amount": 100.0,
  "base": "USD",
  "date": "2025-05-03",
  "rates": {
    "MXN": 1704.53
  }
}
```

The program extracts the `rates[TO]` value and calculates the conversion rate, storing it for further breakdowns (e.g., per hour, per day, etc.).

> 💡 This is a **practical exercise** in API integration and data parsing with Python for beginners in CLI automation, backend development, or scripting.

---


## Model Assumptions

* Standard workday: **8 hours per day**
* Workweek: **5 days**
* Total working weeks per year: **52**
* Total working days per year:

> 52 weeks × 5 days = 260 working days

* Total working hours per year:

> 260 days × 8 hours = 2080 h/year

Also considering possible calendar variations:

> 261 days × 8 hours = 2088 h/year

We use a more balanced value:

> 2084 h/year (average)

> 🔍 However, to improve precision, we use a **more accurate monthly average** based on this annual distribution.

---

## Realistic Monthly Distribution

Distributing the 260 working days across the 12 months of the Gregorian calendar:

```
If you assume 5 working days per week → 5 × 52 = 260
```

> 260 working days / 12 months = 21.6667 working days/month

```
If you account for weekends → 365 - 104 = 261
```

> 261 working days / 12 months = 21.75 working days/month

Multiplied by 8 hours per day:

> 21.6667 × 8 = 173.33 h/month

> 21.75 × 8 = 174 h/month

Final average:

> 173.67 h/month (average)

---

## Work Time Equivalence Table (Average Model)

```python
HOURS_PER_UNIT = {
    "MINUTE": 1 / 60,
    "HOUR": 1,
    "DAY": 8,
    "WEEK": 40,
    "MONTH": 173.6667,
    "YEAR": 2084
}
```

---

## Example Calculation

### Assumption: pay rate of \$0.40 USD per minute

1. Convert to hourly rate:

> 0.40 × 60 = 24.00 USD/hour

2. Annual salary:

> 24.00 × 2084 = 50,016.00 USD/year

3. Compared to a target annual salary of \$50,000 USD:

* **Absolute error**:

> |50,000 - 50,016| = 16 USD

* **Relative error**:

> 16 / 50,000 × 100 = 0.032%

> ✅ Practically negligible error → high accuracy.

---


## Installation and Usage

### Requirements

* Python 3.12 or newer
* [`uv`](https://docs.astral.sh/uv/)
* `make` (optional, for the convenience commands below)

### 1. Clone the repository

```bash
git clone https://github.com/FelipeWoo/salary-calculator-cli.git
cd salary-calculator-cli
```

---

### 2. Make sure you have `uv` installed


```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

---


### 3. Install the project

Install the exact dependencies recorded in `uv.lock`:

```bash
uv sync --locked
```

Alternatively, use the included `Makefile`:

```bash
make install
```

This creates a `.venv` directory and installs the project dependencies.

---

### 4. Activate the virtual environment

```bash
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows CMD
```

---

### 5. Run the application

```bash
uv run python main.py
```

Or:

```bash
make run
```

You will be prompted to enter:

* The salary amount
* The time unit (minute, hour, day, etc.)
* The source currency (e.g., USD)
* The target currency (e.g., MXN)

---

## Development Commands

```bash
make help     # List available commands
make install  # Install locked dependencies
make run      # Run the application
make check    # Check Python syntax
make clean    # Remove generated artifacts
```

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

## Conclusions

* This model maintains consistency across all time units.
* Rounding is minimized, enabling precise salary comparisons.
* A useful tool to evaluate job offers, plan income, or simulate contracts.
* Serves as an educational script to learn about:

  * Time unit normalization
  * Currency exchange integration
  * CLI data entry and output formatting

---