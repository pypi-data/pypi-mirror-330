# HLCalculator

A powerful command-line calculator that supports basic arithmetic, scientific operations, and mathematical constants.

## Features

- Basic arithmetic operations:
  - Addition (+)
  - Subtraction (-)
  - Multiplication (*)
  - Division (/)
  - Power (^)

- Scientific operations:
  - Square root (sqrt)
  - Logarithm (log)
  - Trigonometric functions (sin, cos, tan)
  - Factorial

- Mathematical constants:
  - π (pi)
  - e
  - τ (tau)

## Installation

Using pip:
```bash
pip install hlcalculator
```

Using Poetry:
```bash
poetry add hlcalculator
```

## Usage

The calculator provides two main commands:
- `hlcal calc`: For calculations
- `hlcal const`: For mathematical constants

### Basic Operations

```bash
hlcal calc 5 + 3         # Addition: 8.0
hlcal calc 10 - 4        # Subtraction: 6.0
hlcal calc 3 '*' 4       # Multiplication: 12.0 (use quotes for *)
hlcal calc 15 / 3        # Division: 5.0
hlcal calc 2 ^ 3         # Power: 8.0
```

### Scientific Operations

```bash
hlcal calc 16 sqrt       # Square root: 4.0
hlcal calc 100 log 10    # Log base 10: 2.0
hlcal calc 0.5 sin       # Sine (in radians): 0.479
hlcal calc 5 factorial   # Factorial: 120.0
```

### Mathematical Constants

```bash
hlcal const pi           # π: 3.141592653589793
hlcal const e            # e: 2.718281828459045
hlcal const tau          # τ: 6.283185307179586
```

## Development

### Requirements

- Python 3.12 or higher
- Poetry for dependency management

### Setup Development Environment

1. Clone the repository
```bash
git clone https://github.com/hailv/hlcalculator.git
cd hlcalculator
```

2. Install dependencies
```bash
poetry install
```

3. Activate virtual environment
```bash
poetry shell
```

### Code Quality Tools

The project uses several code quality tools:

- black: Code formatting
- flake8: Style guide enforcement
- mypy: Static type checking
- isort: Import sorting

Run all code quality checks:
```bash
poetry run black .
poetry run flake8 .
poetry run mypy .
poetry run isort .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
