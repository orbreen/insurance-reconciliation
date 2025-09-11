from enum import Enum
from dataclasses import dataclass


class ReconciliationStatus(Enum):
    BALANCED = "BALANCED"
    OVERPAID = "OVERPAID"
    UNDERPAID = "UNDERPAID"


@dataclass
class ReconciliationResult:
    claim_id: int
    patient_id: int
    charges_amount: float
    benefit_amount: float
    total_transaction_value: float
    reconciliation_status: ReconciliationStatus