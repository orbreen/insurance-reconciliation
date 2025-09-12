from datetime import datetime

import polars as pl
from typing import List
from models import ReconciliationStatus, ReconciliationResult


class ReconciliationEngine:
    def __init__(self, claims_file: str, invoices_file: str, tolerance_percentage: float = 5.0):
        self.claims_df = pl.read_csv(claims_file)
        self.invoices_df = pl.read_csv(invoices_file)
        self.tolerance_percentage = tolerance_percentage

    def reconcile(self) -> List[ReconciliationResult]:
        # Group invoices by claim_id and sum transaction values
        invoice_totals = (
            self.invoices_df
            .group_by("claim_id")
            .agg(pl.col("transaction_value").sum().alias("total_transaction_value"))
        )

        # Join claims with invoice totals
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

        # Determine reconciliation status with tolerance
        results = []
        for row in reconciled.iter_rows(named=True):
            benefit = row["benefit_amount"]
            transaction_total = row["total_transaction_value"]

            # Calculate variance percentage
            if benefit != 0:
                variance_percentage = abs((transaction_total - benefit) / benefit) * 100
            else:
                variance_percentage = 0.0 if transaction_total == 0 else float('inf')

            # Determine status
            if benefit == transaction_total:
                status = ReconciliationStatus.BALANCED
            elif variance_percentage <= self.tolerance_percentage:
                status = ReconciliationStatus.NEARLY_BALANCED
            elif transaction_total > benefit:
                status = ReconciliationStatus.OVERPAID
            else:
                status = ReconciliationStatus.UNDERPAID

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

        return results