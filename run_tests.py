# run_tests.py - runs all test files
#
# Josh Meise
# 01-18-2026
# Description: 
#

import sys
import subprocess
from pathlib import Path

ARGC = [1]

if __name__ == "__main__":
    # Parse arguments.
    if len(sys.argv) not in ARGC:
        print("usage: python3 run_tests.py")
        sys.exit(1)

   # Run python unit tests.
    print("Running tests...")
    
    unit_tests = subprocess.run(["python3", "-m", "unittest", "discover", "-s", "tests"], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    
    if unit_tests.returncode != 0:
        print("Tests failed.")
        print("Run \"python3 -m unittest discover -s tests\" in SchemeCompiler directory for further details.")
        print("Ensure that the interpreter has been built prior to running that command.");
    else:
        print("Tests passed.")

