# SWIFT CH20 Reproduction Project

This project reproduces the SWIFT **CH20** error message (*Decimal Points Not Compatible With Currency*) for Japanese Yen (JPY) transactions using an automated ISO 20022 workflow.

## 📁 Project Structure

```text
kamu-swift-prep/
├── data/
│   └── records.csv             # Dynamic payment records (Auto-generated)
├── resources/
│   ├── swift_keywords.resource # Gherkin step definitions
│   └── xml_builder.py          # Professional ISO 20022 XML helper
├── tests/
│   └── swift_tests.robot       # Robot Framework data-driven suite
├── scripts/
│   ├── generate_records.py     # Script to generate mock SWIFT data
│   └── mock_server.py          # Flask-based ISO 20022 mock server
├── run_swift.sh                # Main entry point (highly recommended)
├── requirements.txt            # Project dependencies
└── README.md                   # This project documentation
```

## 🚀 Getting Started

### 1. Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Running the Project (Recommended)
Use the professional wrapper script to automatically generate data and run tests:

```bash
# Run with default 150 records
./run_swift.sh

# Run with custom record count (e.g., 20)
./run_swift.sh --count 20
```

### 3. Manual Steps (Optional)
If you prefer running individual components:

1. **Start Server**: `python3 scripts/mock_server.py`
2. **Generate Data**: `python3 scripts/generate_records.py --count 150`
3. **Run Robot**: `robot tests/swift_tests.robot`

## 📊 Results Summary
- **Success (`ACTC`)**: Non-JPY or integer JPY amounts.
- **CH20 Error (`RJCT`)**: JPY amounts with decimals (rejected by mock server).
- **Artifacts**: Check `report.html` and `log.html` for full SWIFT XML traces.
