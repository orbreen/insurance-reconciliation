from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import ClassVar, Set


class BillType(Enum):
    FEE = "fee"
    PROCEDURE_PAYMENT = "procedure payment"


@dataclass
class Patient:
    patient_id: int
    name: str
    _used_ids: ClassVar[Set[int]] = set()

    def __post_init__(self):
        if self.patient_id in self._used_ids:
            raise ValueError(f"Patient ID {self.patient_id} already exists")
        self._used_ids.add(self.patient_id)


@dataclass
class Claim:
    claim_id: int
    patient_id: int
    date_of_service: datetime
    charges_amount: float
    benefit_amount: float
    _used_ids: ClassVar[Set[int]] = set()

    def __post_init__(self):
        if self.claim_id in self._used_ids:
            raise ValueError(f"Claim ID {self.claim_id} already exists")
        if self.charges_amount <= 0:
            raise ValueError("Charges amount must be > 0")
        if self.benefit_amount > self.charges_amount:
            raise ValueError("Benefit amount cannot exceed charges amount")

        now = datetime.now()
        two_years_ago = now - timedelta(days=731)
        if self.date_of_service > now:
            raise ValueError("Date of service cannot be in the future")
        if self.date_of_service < two_years_ago:
            raise ValueError("Date of service must be within past 2 years")

        self._used_ids.add(self.claim_id)


@dataclass
class Invoice:
    invoice_id: int
    claim_id: int
    type_of_bill: BillType
    transaction_value: float
    _used_ids: ClassVar[Set[int]] = set()

    def __post_init__(self):
        if self.invoice_id in self._used_ids:
            raise ValueError(f"Invoice ID {self.invoice_id} already exists")
        self._used_ids.add(self.invoice_id)