import random
from robot.libraries.BuiltIn import BuiltIn
from DataDriver.AbstractReaderClass import AbstractReaderClass

class data_source(AbstractReaderClass):
    """
    A dynamic data reader for DataDriver that generates records on-the-fly.
    """
    
    def get_data_from_source(self, source=None, include=None, exclude=None):
        # Accessing RECORD_COUNT directly from Robot's variables
        # This works if RECORD_COUNT is passed via -v CLI
        try:
            # We try to get the variable from BuiltIn, which should be available during discovery
            record_count_str = BuiltIn().get_variable_value("${RECORD_COUNT}", "150")
            record_count = int(record_count_str)
        except Exception as e:
            # Fallback for discovery phase if BuiltIn is not fully ready
            print(f"DEBUG: Falling back to default (Exception: {e})")
            record_count = 150
            
        print(f"DEBUG: Generating {record_count} dynamic records for DataDriver...")
        
        # Proportional failure rate (10%)
        num_fails = max(1, int(record_count * 0.1)) if record_count > 0 else 0
        jpy_fail_indices = set(random.sample(range(record_count), num_fails)) if record_count > 0 else set()
        
        currencies = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD"]
        data_list = []
        
        for i in range(record_count):
            record_id = i + 1
            if i in jpy_fail_indices:
                currency = "JPY"
                amount = round(random.uniform(1000, 100000), 2)
                expected_status = "REJECTED"
            else:
                currency = random.choice(currencies)
                if currency == "JPY":
                    amount = random.randint(1000, 100000)
                else:
                    amount = round(random.uniform(10, 5000), 2)
                expected_status = "ACCEPTED"
            
            # Map to ${variable} names for DataDriver
            # Using the ${} syntax is critical for DataDriver variable mapping
            data_list.append({
                "${record_id}": str(record_id),
                "${currency}": currency,
                "${amount}": str(amount),
                "${expected_status}": str(expected_status)
            })
            
        return data_list
