import csv
import random
import os
import argparse

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "records.csv")

# Currencies
CURRENCIES = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD"]

def main():
    parser = argparse.ArgumentParser(description="Generate mock SWIFT payment records.")
    parser.add_argument("-n", "--count", type=int, default=150, help="Total number of records (default: 150)")
    parser.add_argument("-f", "--fail-rate", type=float, default=0.1, help="Percentage of failing JPY records (default: 0.1)")
    args = parser.parse_args()

    total_records = args.count
    # Calculate how many failing JPY records to create (at least 1 if total > 0 and rate > 0)
    num_fails = max(1, int(total_records * args.fail_rate)) if total_records > 0 else 0
    
    # Ensure we don't have more fails than records
    num_fails = min(num_fails, total_records)
    
    jpy_fail_indices = set(random.sample(range(total_records), num_fails)) if total_records > 0 else set()
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, "w", newline='') as csvfile:
        fieldnames = ['${record_id}', '${currency}', '${amount}', '${expected_status}']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(total_records):
            record_id = i + 1
            if i in jpy_fail_indices:
                currency = "JPY"
                # Decimal amounts for JPY cause CH20
                amount = round(random.uniform(1000, 100000), 2)
                expected_status = "REJECTED"
            else:
                # Pick a non-failing currency
                currency = random.choice(CURRENCIES)
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

    print(f"Generated {total_records} records (with {num_fails} failing JPY cases) in '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()
