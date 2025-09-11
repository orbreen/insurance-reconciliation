import random
from datetime import datetime, timedelta
from faker import Faker
from typing import List
from models import Patient, Claim, Invoice, BillType

class DataGenerator:
    def __init__(self, seed: int = 42):
        self.fake = Faker()
        Faker.seed(seed)
        random.seed(seed)
        self.patient_counter = 1
        self.claim_counter = 1
        self.invoice_counter = 1

    def generate_patients(self, count: int = 200) -> List[Patient]:
        patients = []
        for _ in range(count):
            patient = Patient(
                patient_id=self.patient_counter,
                name=self.fake.name()
            )
            patients.append(patient)
            self.patient_counter += 1
        return patients

    def generate_claims_for_patient(self, patient_id: int) -> List[Claim]:
        claim_count = random.randint(2, 20)
        claims = []

        for _ in range(claim_count):
            charges = round(random.uniform(0.01, 1000000.0), 2)
            benefit = round(random.uniform(0.01, charges), 2)

            claim = Claim(
                claim_id=self.claim_counter,
                patient_id=patient_id,
                date_of_service=self._random_date_past_2_years(),
                charges_amount=charges,
                benefit_amount=benefit
            )
            claims.append(claim)
            self.claim_counter += 1

        return claims

    def generate_invoices_for_claim(self, claim_id: int) -> List[Invoice]:
        invoice_count = random.randint(1, 5)
        invoices = []

        for _ in range(invoice_count):
            invoice = Invoice(
                invoice_id=self.invoice_counter,
                claim_id=claim_id,
                type_of_bill=random.choice(list(BillType)),
                transaction_value=round(random.uniform(-1000000.0, 2000000.0), 2)
            )
            invoices.append(invoice)
            self.invoice_counter += 1

        return invoices

    def _random_date_past_2_years(self) -> datetime:
        now = datetime.now()
        random_days = random.randint(0, 730)
        return now - timedelta(days=random_days)