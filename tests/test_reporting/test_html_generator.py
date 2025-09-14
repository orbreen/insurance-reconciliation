import tempfile
import os
from datetime import datetime
from reporting.html_generator import HTMLReportGenerator
from reconciliation_engine.models import ReconciliationResult, ReconciliationStatus


class TestHTMLReportGenerator:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.output_file = os.path.join(self.temp_dir, 'test_report.html')
        self.generator = HTMLReportGenerator()

        self.sample_results = [
            ReconciliationResult(1, 1, datetime(2024, 1, 15), 1000.0, 800.0, 800.0, ReconciliationStatus.BALANCED, 0.0),
            ReconciliationResult(2, 1, datetime(2024, 2, 20), 500.0, 400.0, 420.0, ReconciliationStatus.OVERPAID, 5.0)
        ]

    def teardown_method(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        os.rmdir(self.temp_dir)

    def test_report_generation(self):
        self.generator.generate_report(self.sample_results, self.output_file)

        assert os.path.exists(self.output_file)

        with open(self.output_file, 'r') as f:
            content = f.read()

        assert 'Insurance Claims Reconciliation Report' in content
        assert 'chart.js' in content
        assert '2024-01-15' in content