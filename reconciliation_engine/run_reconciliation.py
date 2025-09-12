from engine import ReconciliationEngine
import sys
sys.path.append('.')
from reporting.html_generator import HTMLReportGenerator


def main():
    print("Starting reconciliation...")

    # Initialize engine with CSV files and 5% tolerance
    engine = ReconciliationEngine(
        claims_file="data/fake_data/claims.csv",
        invoices_file="data/fake_data/invoices.csv",
        tolerance_percentage=5.0
    )

    # Run reconciliation
    results = engine.reconcile()

    # Print summary to console
    total_claims = len(results)
    balanced = sum(1 for r in results if r.reconciliation_status.value == "BALANCED")
    nearly_balanced = sum(1 for r in results if r.reconciliation_status.value == "NEARLY_BALANCED")
    overpaid = sum(1 for r in results if r.reconciliation_status.value == "OVERPAID")
    underpaid = sum(1 for r in results if r.reconciliation_status.value == "UNDERPAID")

    print(f"Total claims processed: {total_claims}")
    print(f"Balanced: {balanced}")
    print(f"Nearly Balanced (±5%): {nearly_balanced}")
    print(f"Overpaid: {overpaid}")
    print(f"Underpaid: {underpaid}")

    # Show interesting insight
    nearly_or_balanced = balanced + nearly_balanced
    percentage = round((nearly_or_balanced / total_claims) * 100, 1) if total_claims > 0 else 0
    print(f"\n💡 Insight: {nearly_or_balanced} claims ({percentage}%) are within 5% of being perfectly balanced!")

    # Generate HTML report
    print("\nGenerating HTML report...")
    report_generator = HTMLReportGenerator()
    report_generator.generate_report(results)

    print("Reconciliation complete!")


if __name__ == "__main__":
    main()