import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .engine import ReconciliationEngine
from reporting.html_generator import HTMLReportGenerator


def main():
    engine = ReconciliationEngine(
        claims_file="data/fake_data/claims.csv",
        invoices_file="data/fake_data/invoices.csv",
        tolerance_percentage=5.0
    )
    results = engine.reconcile()
    report_generator = HTMLReportGenerator()
    report_generator.generate_report(results)

if __name__ == "__main__":
    main()