from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class ReconciliationStatus(Enum):
    BALANCED = "BALANCED"
    NEARLY_BALANCED = "NEARLY_BALANCED"
    OVERPAID = "OVERPAID"
    UNDERPAID = "UNDERPAID"


@dataclass
class ReconciliationResult:
    claim_id: int
    patient_id: int
    date_of_service: datetime
    charges_amount: float
    benefit_amount: float
    total_transaction_value: float
    reconciliation_status: ReconciliationStatus
    variance_percentage: float = 0.0