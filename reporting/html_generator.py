from jinja2 import Environment, FileSystemLoader
from typing import List
from reconciliation_engine.models import ReconciliationResult, ReconciliationStatus


class HTMLReportGenerator:
    def __init__(self, template_dir: str = "reporting/templates"):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate_report(self, results: List[ReconciliationResult], output_file: str = "output/report.html"):
        # Calculate summary statistics
        total_claims = len(results)
        balanced_count = sum(1 for r in results if r.reconciliation_status.value == "BALANCED")
        overpaid_count = sum(1 for r in results if r.reconciliation_status.value == "OVERPAID")
        underpaid_count = sum(1 for r in results if r.reconciliation_status.value == "UNDERPAID")

        # Calculate percentages
        balanced_percentage = round((balanced_count / total_claims) * 100, 1) if total_claims > 0 else 0
        overpaid_percentage = round((overpaid_count / total_claims) * 100, 1) if total_claims > 0 else 0
        underpaid_percentage = round((underpaid_count / total_claims) * 100, 1) if total_claims > 0 else 0

        # Prepare template data
        template_data = {
            'total_claims': total_claims,
            'balanced_count': balanced_count,
            'balanced_percentage': balanced_percentage,
            'overpaid_count': overpaid_count,
            'overpaid_percentage': overpaid_percentage,
            'underpaid_count': underpaid_count,
            'underpaid_percentage': underpaid_percentage,
            'results': results
        }

        # Render template
        template = self.env.get_template('report_template.html')
        html_content = template.render(template_data)

        # Write to file
        with open(output_file, 'w') as f:
            f.write(html_content)

        print(f"HTML report generated: {output_file}")