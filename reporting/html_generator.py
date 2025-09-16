from jinja2 import Environment, FileSystemLoader
from typing import List
from reconciliation_engine.models import ReconciliationResult, ReconciliationStatus
from utils.logger import setup_logger


class HTMLReportGenerator:
    def __init__(self, template_dir: str = "reporting/templates"):
        self.logger = setup_logger(self.__class__.__name__)
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.logger.info(f"Initialized HTML generator with template directory: {template_dir}")

    def generate_report(self, results: List[ReconciliationResult], output_file: str = "output/report.html"):
        self.logger.info(f"Generating HTML report for {len(results)} results")

        total_claims = len(results)
        balanced_count = sum(1 for r in results if r.reconciliation_status.value == "BALANCED")
        nearly_balanced_count = sum(1 for r in results if r.reconciliation_status.value == "NEARLY_BALANCED")
        overpaid_count = sum(1 for r in results if r.reconciliation_status.value == "OVERPAID")
        underpaid_count = sum(1 for r in results if r.reconciliation_status.value == "UNDERPAID")

        balanced_percentage = round((balanced_count / total_claims) * 100, 1) if total_claims > 0 else 0
        nearly_balanced_percentage = round((nearly_balanced_count / total_claims) * 100, 1) if total_claims > 0 else 0
        overpaid_percentage = round((overpaid_count / total_claims) * 100, 1) if total_claims > 0 else 0
        underpaid_percentage = round((underpaid_count / total_claims) * 100, 1) if total_claims > 0 else 0

        self.logger.info(
            f"Report statistics - Balanced: {balanced_count}, Nearly Balanced: {nearly_balanced_count}, Overpaid: {overpaid_count}, Underpaid: {underpaid_count}")

        template_data = {
            'total_claims': total_claims,
            'balanced_count': balanced_count,
            'balanced_percentage': balanced_percentage,
            'nearly_balanced_count': nearly_balanced_count,
            'nearly_balanced_percentage': nearly_balanced_percentage,
            'overpaid_count': overpaid_count,
            'overpaid_percentage': overpaid_percentage,
            'underpaid_count': underpaid_count,
            'underpaid_percentage': underpaid_percentage,
            'results': results
        }

        try:
            template = self.env.get_template('report_template.html')
            html_content = template.render(template_data)

            with open(output_file, 'w') as f:
                f.write(html_content)

            self.logger.info(f"HTML report successfully generated: {output_file}")
        except Exception as e:
            self.logger.error(f"Failed to generate HTML report: {e}")
            raise