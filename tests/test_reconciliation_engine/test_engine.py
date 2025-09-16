import pytest
import tempfile
import os
from reconciliation_engine.engine import ReconciliationEngine
from reconciliation_engine.models import ReconciliationStatus


class TestReconciliationEngine:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.claims_file = os.path.join(self.temp_dir, 'test_claims.csv')
        self.invoices_file = os.path.join(self.temp_dir, 'test_invoices.csv')

        claims_csv = """claim_id,patient_id,date_of_service,charges_amount,benefit_amount
1,1,2024-01-15,1000.00,800.00
2,1,2024-02-20,500.00,400.00
3,2,2024-03-10,750.00,600.00"""

        invoices_csv = """invoice_id,claim_id,type_of_bill,transaction_value
1,1,fee,800.00
2,2,fee,420.00
3,2,procedure payment,-20.00
4,3,fee,550.00"""

        with open(self.claims_file, 'w') as f:
            f.write(claims_csv)
        with open(self.invoices_file, 'w') as f:
            f.write(invoices_csv)

    def teardown_method(self):
        os.remove(self.claims_file)
        os.remove(self.invoices_file)
        os.rmdir(self.temp_dir)

    def test_reconciliation_statuses(self):
        engine = ReconciliationEngine(self.claims_file, self.invoices_file)
        results = engine.reconcile()

        assert len(results) == 3
        assert results[0].reconciliation_status == ReconciliationStatus.BALANCED
        assert results[1].reconciliation_status == ReconciliationStatus.BALANCED
        assert results[2].reconciliation_status == ReconciliationStatus.UNDERPAID
        assert results[2].variance_percentage == 8.33

    def test_tolerance_feature(self):
        engine = ReconciliationEngine(self.claims_file, self.invoices_file, tolerance_percentage=10.0)
        results = engine.reconcile()

        assert results[2].reconciliation_status == ReconciliationStatus.NEARLY_BALANCED