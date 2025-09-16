import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import polars as pl
from data.data_generation.generator import DataGenerator
from utils.logger import setup_logger


def main():
    logger = setup_logger("DataGenerator")
    
    os.makedirs("data/fake_data", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    logger.info("Starting data generation process")
    generator = DataGenerator()

    logger.info("Generating 200 patients...")
    patients = generator.generate_patients(200)

    logger.info("Generating claims and invoices...")
    all_claims = []
    all_invoices = []

    for patient in patients:
        claims = generator.generate_claims_for_patient(patient.patient_id)
        all_claims.extend(claims)

        for claim in claims:
            invoices = generator.generate_invoices_for_claim(claim.claim_id)
            all_invoices.extend(invoices)

    logger.info(f"Generated {len(all_claims)} claims and {len(all_invoices)} invoices")

    claims_data = [
        {
            "claim_id": claim.claim_id,
            "patient_id": claim.patient_id,
            "date_of_service": claim.date_of_service.strftime("%Y-%m-%d"),
            "charges_amount": claim.charges_amount,
            "benefit_amount": claim.benefit_amount
        }
        for claim in all_claims
    ]

    invoices_data = [
        {
            "invoice_id": invoice.invoice_id,
            "claim_id": invoice.claim_id,
            "type_of_bill": invoice.type_of_bill.value,
            "transaction_value": invoice.transaction_value
        }
        for invoice in all_invoices
    ]

    claims_df = pl.DataFrame(claims_data)
    invoices_df = pl.DataFrame(invoices_data)

    try:
        claims_df.write_csv("data/fake_data/claims.csv")
        invoices_df.write_csv("data/fake_data/invoices.csv")
        logger.info("CSV files saved successfully")
    except Exception as e:
        logger.error(f"Failed to save CSV files: {e}")
        raise


if __name__ == "__main__":
    main()
