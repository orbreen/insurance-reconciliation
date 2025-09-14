import pytest
from datetime import datetime, timedelta
from data.data_generation.models import Patient, Claim, Invoice, BillType


class TestPatient:
    def setup_method(self):
        Patient._used_ids.clear()

    def test_patient_creation_and_unique_ids(self):
        patient1 = Patient(1, "Or Breen")
        assert patient1.patient_id == 1
        assert patient1.name == "Or Breen"

        with pytest.raises(ValueError, match="Patient ID 1 already exists"):
            Patient(1, "Or Been")


class TestClaim:
    def setup_method(self):
        Claim._used_ids.clear()

    def test_claim_validations(self):
        date = datetime.now() - timedelta(days=100)

        # Valid claim
        claim = Claim(1, 1, date, 1000.0, 800.0)
        assert claim.charges_amount == 1000.0

        # Test validations
        with pytest.raises(ValueError, match="Claim ID 1 already exists"):
            Claim(1, 2, date, 500.0, 400.0)

        with pytest.raises(ValueError, match="Charges amount must be > 0"):
            Claim(2, 1, date, 0.0, 100.0)

        with pytest.raises(ValueError, match="Benefit amount cannot exceed charges amount"):
            Claim(3, 1, date, 500.0, 600.0)


class TestInvoice:
    def setup_method(self):
        Invoice._used_ids.clear()

    def test_invoice_creation_and_enum(self):
        invoice = Invoice(1, 1, BillType.FEE, 250.0)
        assert invoice.transaction_value == 250.0
        assert invoice.type_of_bill.value == "fee"

        with pytest.raises(ValueError, match="Invoice ID 1 already exists"):
            Invoice(1, 2, BillType.PROCEDURE_PAYMENT, 300.0)