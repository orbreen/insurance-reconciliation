import polars as pl
from generator import DataGenerator


def main():
    generator = DataGenerator()

    print("Generating 200 patients...")
    patients = generator.generate_patients(200)

    print("Generating claims and invoices...")
    all_claims = []
    all_invoices = []

    for patient in patients:
        claims = generator.generate_claims_for_patient(patient.patient_id)
        all_claims.extend(claims)

        for claim in claims:
            invoices = generator.generate_invoices_for_claim(claim.claim_id)
            all_invoices.extend(invoices)

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

    claims_df.write_csv("data/fake_data/claims.csv")
    invoices_df.write_csv("data/fake_data/invoices.csv")

    print(f"Generated {len(claims_data)} claims and {len(invoices_data)} invoices")

if __name__ == "__main__":
    main()