# 401k Retirement Plan System

A Python object-oriented programming project implementing a 401k retirement benefit calculator for production workers and shift supervisors, built on a multi-level class inheritance hierarchy.

---

## Overview

This project models a factory employee payroll system extended with 401k retirement matching logic. It demonstrates core OOP principles including inheritance, encapsulation, class methods, and input validation — built entirely from scratch without external libraries.

---

## Class Hierarchy

```
Employee
├── ProductionWorker
│   └── PW401k          ← hourly worker with 401k plan
└── ShiftSupervisor
    └── S401k           ← salaried supervisor with 401k plan
```

- **`Employee`** — base class with name, number, and benefits eligibility
- **`ProductionWorker`** — adds shift, hourly pay rate, and hours worked
- **`ShiftSupervisor`** — adds annual salary, shift, and a managed worker roster
- **`PW401k`** — extends `ProductionWorker` with 401k account, contribution, and employer match calculation
- **`S401k`** — extends `ShiftSupervisor` with the same 401k logic, based on monthly salary

---

## Features

- **Employer match logic** — calculates the maximum match (5% of monthly pay) and the actual match (lesser of contribution or max match)
- **Auto-generated account numbers** — each employee receives a unique 6-character account ID on instantiation
- **Full input validation** — all setters validate type and range, returning `True`/`False` without raising exceptions
- **Benefits eligibility** — automatically assigned based on employee number (< 500 = eligible)
- **Shift enum** — `DAY`, `SWING`, and `NIGHT` shifts enforced via `Shift(Enum)`
- **Supervisor roster management** — supervisors can add up to `max_workers` workers with shift-match enforcement and capacity checks
- **Bonus trigger** — supervisors with 5+ workers earn a $10,000 salary bonus via `bonus()`
- **`__str__` methods** — each class has a clean, formatted string output; subclasses return `""` when called on a parent type

---

## How It Works

### 401k Match Calculation

| Role | Monthly Pay Basis | Max Match | Actual Match |
|---|---|---|---|
| `PW401k` | `gross_pay() × 4` | 5% of monthly pay | `min(contribution, max_match)` |
| `S401k` | `salary / 12` | 5% of monthly pay | `min(contribution, max_match)` |

### Example Output

```
John Smith  #578
Account #dkw578
Monthly pay: $2,100.00
Amount contributed: $500.00
Max match: $105.00
Actual match: $105.00
```

---

## Getting Started

**Requirements:** Python 3.7+

```bash
# Clone the repo
git clone https://github.com/your-username/401k-retirement-system.git
cd 401k-retirement-system

# Run the demo
python Lab_Assignment_7.py
```

No external dependencies — uses only Python standard library (`random`, `enum`).

---

## Sample Usage

```python
from Lab_Assignment_7 import PW401k, S401k, Shift

# Create a production worker with 401k
worker = PW401k(name='Jane Doe', number=450,
                shift=Shift.DAY, pay_rate=18, hours=40,
                contribution=300)

print(worker.get_max_match())   # 144.0
print(worker.get_actual_match()) # 144.0

# Create a supervisor with 401k
supervisor = S401k(name='Bob Ray', number=210,
                   salary=120000, shift=Shift.DAY,
                   contribution=400)

print(supervisor.monthly_pay())  # 10000.0
print(supervisor.get_max_match()) # 500.0
```

---

## Project Structure

```
401k-retirement-system/
│
├── Lab_Assignment_7.py   # All classes + main() demo
└── README.md
```

---

## Concepts Demonstrated

- Multi-level class inheritance with `super()`
- `**kwargs` pass-through for cooperative multiple inheritance
- `@classmethod` validators and `@staticmethod` utilities
- Python `Enum` for constrained categorical values
- Encapsulation with private attributes (`_account`, `_contribution`, `_max_match`)
- Guard clauses and defensive programming patterns

---

## Author

**Tatsiana Chakhovich** — QA Automation Engineer  

