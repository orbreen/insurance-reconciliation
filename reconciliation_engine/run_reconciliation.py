from engine import ReconciliationEngine
import sys
sys.path.append('.')
from reporting.html_generator import HTMLReportGenerator


def main():
    print("Starting reconciliation...")

    # Initialize engine with CSV files
    engine = ReconciliationEngine(
        claims_file="data/fake_data/claims.csv",
        invoices_file="data/fake_data/invoices.csv"
    )

    # Run reconciliation
    results = engine.reconcile()

    # Print summary to console
    total_claims = len(results)
    balanced = sum(1 for r in results if r.reconciliation_status.value == "BALANCED")
    overpaid = sum(1 for r in results if r.reconciliation_status.value == "OVERPAID")
    underpaid = sum(1 for r in results if r.reconciliation_status.value == "UNDERPAID")

    print(f"Total claims processed: {total_claims}")
    print(f"Balanced: {balanced}")
    print(f"Overpaid: {overpaid}")
    print(f"Underpaid: {underpaid}")

    # Generate HTML report
    print("\nGenerating HTML report...")
    report_generator = HTMLReportGenerator()
    report_generator.generate_report(results)

    print("Reconciliation complete!")


if __name__ == "__main__":
    main()