# Insurance Claims Reconciliation Engine

A Python application that matches insurance claims with invoices to identify payment discrepancies.

## Quick Start

1. Install: `pip3 install -r requirements.txt`
2. Generate data: `python3 data/data_generation/generate_data.py`
3. Run reconciliation: `python3 reconciliation_engine/run_reconciliation.py`
4. View report: `open output/report.html`

## Features

- **Tolerance analysis** for "nearly balanced" claims
- **Interactive visualizations** with Chart.js (variance distribution, timeline)
- **Comprehensive logging** with file output and daily rotation
- **Unit test suite** (6 tests covering all components)

## Technologies

Python 3.8+, Polars, Faker, Jinja2, Chart.js, Pytest

## Testing

Run tests: `python3 run_tests.py`

## Author

Or Breen - Fullstack Developer Assignment
