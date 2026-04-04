import csv
import random
import os

# Configuration
TOTAL_RECORDS = 150
FAILING_JPY_RECORDS = 15
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "records.csv")

# Currencies
CURRENCIES = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD"]

def main():
    """Generates 150 mock payment records with DataDriver-friendly headers."""
    jpy_fail_indices = set(random.sample(range(TOTAL_RECORDS), FAILING_JPY_RECORDS))
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, "w", newline='') as csvfile:
        # Reverting to ${} headers as it's the most reliable for DataDriver variable mapping
        fieldnames = ['${record_id}', '${currency}', '${amount}', '${expected_status}']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(TOTAL_RECORDS):
            record_id = i + 1
            if i in jpy_fail_indices:
                currency = "JPY"
                amount = round(random.uniform(1000, 100000), 2)
                expected_status = "REJECTED"
            else:
                currency = random.choice([c for c in CURRENCIES if c != "JPY" or i not in jpy_fail_indices])
                if currency == "JPY":
                    amount = random.randint(1000, 100000)
                else:
                    amount = round(random.uniform(10, 5000), 2)
                expected_status = "ACCEPTED"
            
            writer.writerow({
                '${record_id}': record_id,
                '${currency}': currency,
                '${amount}': amount,
                '${expected_status}': expected_status
            })

    print(f"Generated {TOTAL_RECORDS} records in '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()
