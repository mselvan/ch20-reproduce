from flask import Flask, request, jsonify
from lxml import etree
import re

app = Flask(__name__)

# SWIFT Error Code CH20: Decimal Points Not Compatible With Currency
# JPY is a zero-decimal currency.

def validate_swift_amount(currency, amount_str):
    """
    Validates if the amount is compatible with the currency.
    Returns (True, None) if valid, (False, "CH20") if invalid.
    """
    if currency == "JPY":
        # Check if the amount has any decimal parts (even .00 is technically problematic in some SWIFT contexts, 
        # but usually it's non-zero decimals that trigger CH20)
        if "." in amount_str:
            decimal_part = amount_str.split(".")[1]
            if decimal_part and int(decimal_part) > 0:
                return False, "CH20"
            # In some systems, even "100.00" for JPY is an error.
            # Let's be strict for this reproduction.
            return False, "CH20"
    return True, None

@app.route('/upload', methods=['POST'])
def upload_swift_message():
    xml_data = request.data
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.fromstring(xml_data, parser)
        
        # Namespace handling
        ns = {'n': 'urn:iso:std:iso:20022:tech:xsd:pain.001.001.03'}
        
        # Find currency and amount
        instd_amt = root.xpath('//n:InstdAmt', namespaces=ns)
        if not instd_amt:
            return jsonify({"status": "ERROR", "error": "MISSING_DATA"}), 400
        
        element = instd_amt[0]
        currency = element.get('Ccy')
        amount_str = element.text
        
        is_valid, error_code = validate_swift_amount(currency, amount_str)
        
        if not is_valid:
            print(f"Validation FAILED: {currency} {amount_str} -> {error_code}")
            return jsonify({
                "status": "REJECTED",
                "error_code": error_code,
                "message": f"Decimal points not compatible with currency {currency}"
            }), 400
        
        print(f"Validation SUCCESS: {currency} {amount_str}")
        return jsonify({
            "status": "ACCEPTED",
            "message": "Payment accepted"
        }), 200

    except Exception as e:
        print(f"Error processing XML: {e}")
        return jsonify({"status": "ERROR", "error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Mock SWIFT Server on port 5005...")
    app.run(port=5005)
