# Insurance Claims Reconciliation Engine

A Python application that matches insurance claims with invoices to identify payment discrepancies.

## Quick Start

1. Install dependencies: `pip3 install -r requirements.txt`
2. Generate test data: `python3 data/data_generation/generate_data.py`
3. Run reconciliation: `python3 reconciliation_engine/run_reconciliation.py`
4. View report: `open output/report.html`

## What it does

- Processes insurance claims and invoices
- Identifies balanced, overpaid, and underpaid claims
- Generates HTML reports with statistics

## Technologies

- Python 3.8+
- Polars for data processing
- Faker for test data
- Jinja2 for HTML templating

## Author

Or Breen - Fullstack Developer Assignment
