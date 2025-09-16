import polars as pl
from typing import List
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .models import ReconciliationStatus, ReconciliationResult
from utils.logger import setup_logger


class ReconciliationEngine:
    def __init__(self, claims_file: str, invoices_file: str, tolerance_percentage: float = 5.0):
        self.logger = setup_logger(self.__class__.__name__)
        self.tolerance_percentage = tolerance_percentage

        self.logger.info(f"Initializing ReconciliationEngine with tolerance: {tolerance_percentage}%")

        try:
            self.claims_df = pl.read_csv(claims_file)
            self.invoices_df = pl.read_csv(invoices_file)
            self.logger.info(f"Loaded {len(self.claims_df)} claims and {len(self.invoices_df)} invoices")
        except Exception as e:
            self.logger.error(f"Failed to load CSV files: {e}")
            raise

    def reconcile(self) -> List[ReconciliationResult]:
        self.logger.info("Starting reconciliation process")

        invoice_totals = (
            self.invoices_df
            .group_by("claim_id")
            .agg(pl.col("transaction_value").sum().alias("total_transaction_value"))
        )

        reconciled = (
            self.claims_df
            .join(invoice_totals, on="claim_id", how="left")
            .with_columns(
                pl.when(pl.col("total_transaction_value").is_null())
                .then(0.0)
                .otherwise(pl.col("total_transaction_value"))
                .alias("total_transaction_value")
            )
        )

        results = []
        status_counts = {"BALANCED": 0, "NEARLY_BALANCED": 0, "OVERPAID": 0, "UNDERPAID": 0}

        for row in reconciled.iter_rows(named=True):
            benefit = row["benefit_amount"]
            transaction_total = row["total_transaction_value"]

            if benefit != 0:
                variance_percentage = abs((transaction_total - benefit) / benefit) * 100
            else:
                variance_percentage = 0.0 if transaction_total == 0 else float('inf')

            if benefit == transaction_total:
                status = ReconciliationStatus.BALANCED
            elif variance_percentage <= self.tolerance_percentage:
                status = ReconciliationStatus.NEARLY_BALANCED
            elif transaction_total > benefit:
                status = ReconciliationStatus.OVERPAID
            else:
                status = ReconciliationStatus.UNDERPAID

            status_counts[status.value] += 1

            results.append(ReconciliationResult(
                claim_id=row["claim_id"],
                patient_id=row["patient_id"],
                date_of_service=datetime.strptime(row["date_of_service"], "%Y-%m-%d"),
                charges_amount=row["charges_amount"],
                benefit_amount=benefit,
                total_transaction_value=transaction_total,
                reconciliation_status=status,
                variance_percentage=round(variance_percentage, 2)
            ))

        self.logger.info(f"Reconciliation completed. Results: {status_counts}")
        return results