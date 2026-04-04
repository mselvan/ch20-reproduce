# SWIFT CH20 Reproduction Project

This project reproduces the SWIFT **CH20** error message (*Decimal Points Not Compatible With Currency*) specifically for Japanese Yen (JPY) transactions. 

It demonstrates how 15 out of 150 records failed during an automation test because JPY is a zero-decimal currency, but the payments were sent with fractional amounts.

## 📁 Project Structure

```text
kamu-swift-prep/
├── data/
│   └── records.csv             # 150 payment records (Source Data)
├── resources/
│   ├── swift_keywords.resource # Gherkin (BDD) keyword definitions
│   └── xml_builder.py          # Helper library for XML construction
├── tests/
│   └── swift_tests.robot       # Robot Framework test suite (Data Driven)
├── scripts/
│   ├── generate_records.py     # Script to generate mock CSV data
│   └── mock_server.py          # Flask-based mock SWIFT server
├── venv/                       # Virtual environment (ignored by git)
├── requirements.txt            # Project dependencies
└── README.md                   # This project documentation
```

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9 or higher
- `pip` (Python package installer)

### 2. Installation
Clone the repository and set up the virtual environment:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Project

To reproduce the scenario, follow these steps in separate terminal windows (or background them):

#### Step A: Start the Mock SWIFT Server
This server simulates the SWIFT validation rules and will return `CH20` for invalid JPY payments.
```bash
python3 scripts/mock_server.py
```

#### Step B: Generate Mock Data
This script creates a CSV file with 150 records, including 15 failing cases.
```bash
python3 scripts/generate_records.py
```

#### Step C: Run the Robot Framework Tests
Execute the data-driven BDD tests:
```bash
robot tests/swift_tests.robot
```

## 📊 Viewing Results

After running the tests, check the generated artifacts:
- **`report.html`**: High-level summary of pass/fail status.
- **`log.html`**: Detailed execution logs, including:
    - Generated SWIFT XML messages.
    - API request and response data.
    - Specific validation failure reasons for `CH20`.

## 🛠️ Tech Stack
- **Robot Framework**: Core automation framework.
- **DataDriver**: For CSV-to-Test mapping.
- **Flask**: For mocking the SWIFT backend.
- **Gherkin**: For human-readable test cases.
