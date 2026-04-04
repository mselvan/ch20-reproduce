import argparse
import subprocess
import os
import sys

def main():
    """
    Main entry point for running the SWIFT CH20 reproduction tests.
    This script orchestrates data generation and test execution in a cross-platform way.
    """
    parser = argparse.ArgumentParser(description="Professional SWIFT Reproduction Test Runner")
    parser.add_argument("-n", "--count", type=str, default="150", 
                        help="Number of records to generate and run (default: 150)")
    args = parser.parse_args()

    # Determine command paths based on OS
    python_cmd = sys.executable
    
    print(f"--- Preparing SWIFT Reproduction Test (Records: {args.count}) ---")
    
    # 1. Generate the records
    gen_script = os.path.join("scripts", "generate_records.py")
    print(f"Step 1: Generating data...")
    try:
        subprocess.run([python_cmd, gen_script, "--count", args.count], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during data generation: {e}")
        sys.exit(1)
        
    # 2. Run the Robot Framework tests
    robot_file = os.path.join("tests", "swift_tests.robot")
    print(f"Step 2: Executing Robot Framework tests...")
    try:
        # Robot command is usually available in the environment path if installed
        # We try to run it via the current python executable to ensure venv usage
        subprocess.run([python_cmd, "-m", "robot", robot_file], check=True)
    except subprocess.CalledProcessError as e:
        # Robot exits with non-zero if tests fail, but we want the overall flow to be clear
        print(f"Test execution complete (some tests may have failed).")
        
    print(f"--- SWIFT Reproduction Completed ---")

if __name__ == "__main__":
    main()
