#!/bin/bash

# Default values
COUNT=150

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -n|--count) COUNT="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

echo "⚙️ Preparing SWIFT Reproduction Test (Records: $COUNT)..."

# 1. Activate venv if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 2. Generate records with the requested count
python3 scripts/generate_records.py --count "$COUNT"

# 3. Run the Robot Framework suite
# We run from the root, targeting the robot file
robot tests/swift_tests.robot

echo "✅ SWIFT Reproduction Completed."
