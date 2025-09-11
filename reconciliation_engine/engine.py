import polars as pl
from typing import List
from models import ReconciliationStatus, ReconciliationResult


class ReconciliationEngine:
    def __init__(self, claims_file: str, invoices_file: str):
        self.claims_df = pl.read_csv(claims_file)
        self.invoices_df = pl.read_csv(invoices_file)

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

        # Determine reconciliation status
        results = []
        for row in reconciled.iter_rows(named=True):
            if row["benefit_amount"] == row["total_transaction_value"]:
                status = ReconciliationStatus.BALANCED
            elif row["total_transaction_value"] > row["benefit_amount"]:
                status = ReconciliationStatus.OVERPAID
            else:
                status = ReconciliationStatus.UNDERPAID

            results.append(ReconciliationResult(
                claim_id=row["claim_id"],
                patient_id=row["patient_id"],
                charges_amount=row["charges_amount"],
                benefit_amount=row["benefit_amount"],
                total_transaction_value=row["total_transaction_value"],
                reconciliation_status=status
            ))

        return results