# Annual Work Time Calculation (Realistic Average Model)

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

$$
52 \text{ weeks} × 5 \text{ days} = \boxed{260 \text{ working days}}
$$

* Total working hours per year:

$$
260 \text{ days} × 8 \text{ hours} = \boxed{2080 \text{ h/year}}
$$

Also considering possible calendar variations:

$$
261 \text{ days} × 8 \text{ hours} = \boxed{2088 \text{ h/year}}
$$

We use a more balanced value:

$$
\boxed{2084 \text{ h/year (average)}}
$$

> 🔍 However, to improve precision, we use a **more accurate monthly average** based on this annual distribution.

---

## Realistic Monthly Distribution

Distributing the 260 working days across the 12 months of the Gregorian calendar:

```
If you assume 5 working days per week → 5 × 52 = 260
```

$$
\frac{260 \text{ working days}}{12 \text{ months}} = \boxed{21.6667 \text{ working days/month}}
$$

```
If you account for weekends → 365 - 104 = 261
```

$$
\frac{261 \text{ working days}}{12 \text{ months}} = \boxed{21.75 \text{ working days/month}}
$$

Multiplied by 8 hours per day:

$$
21.6667 × 8 = \boxed{173.33 \text{ h/month}}
$$

$$
21.75 × 8 = \boxed{174 \text{ h/month}}
$$

Final average:

$$
\boxed{173.67 \text{ h/month (average)}}
$$

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

$$
0.40 × 60 = \boxed{24.00 \text{ USD/hour}}
$$

2. Annual salary:

$$
24.00 × 2084 = \boxed{50,016.00 \text{ USD/year}}
$$

3. Compared to a target annual salary of \$50,000 USD:

* **Absolute error**:

$$
|50,000 - 50,016| = \boxed{16 \text{ USD}}
$$

* **Relative error**:

$$
\frac{16}{50,000} × 100 = \boxed{0.032\%}
$$

✅ Practically negligible error → high accuracy.

---


## How to Load `pyproject.toml` and Recreate the Environment with `uv`


### 1. Clone the repository

```bash
git clone https://github.com/FelipeWoo/SALARY_CALCULATOR_CLI.git
cd SALARY_CALCULATOR_CLI
```

---

### 2. Make sure you have `uv` installed


```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

---


### 3. Recreate the environment using `uv`

Make sure you have [`uv`](https://github.com/astral-sh/uv) installed. Then run:

```bash
uv venv
uv pip install .
```

This will:

* Create a `.venv` folder (your isolated Python environment)
* Install the project dependencies defined in `pyproject.toml`

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

You will be prompted to enter:

* The salary amount
* The time unit (minute, hour, day, etc.)
* The source currency (e.g., USD)
* The target currency (e.g., MXN)

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