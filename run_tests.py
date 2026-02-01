# run_tests.py - runs all test files
#
# Josh Meise
# 01-18-2026
# Description: 
#

import sys
import subprocess
from pathlib import Path
import os

ARGC = [1]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTERPRETER_UTILS_DIR = os.path.join(BASE_DIR, "interpreter", "utils")
INTERPRETER_EXECS_DIR = os.path.join(BASE_DIR, "interpreter", "execs")

if __name__ == "__main__":
    # Parse arguments.
    if len(sys.argv) not in ARGC:
        print("usage: python3 run_tests.py")
        sys.exit(1)

    # Build interpreter.
    make_utils = subprocess.run(["make clean; make"], cwd = INTERPRETER_UTILS_DIR, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    make_execs = subprocess.run(["make clean; make"], cwd = INTERPRETER_EXECS_DIR, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    
    if make_utils.returncode != 0:
        print("Failed to build interpreter library.")
        sys.exit(1)

    if make_execs.returncode != 0:
        print("Failed to build interpreter executables.")
        sys.exit(1)

    # Run python unit tests.
    print("Running tests...")
    
    unit_tests = subprocess.run(["python3", "-m", "unittest", "discover", "-s", "tests"])
    
    if unit_tests.returncode != 0:
        print("Tests failed.")
        print("Run \"python3 -m unittest discover -s tests\" in SchemeCompiler directory for further details.")
        print("Ensure that the interpreter has been built prior to running that command.");
    else:
        print("Tests passed.")

    # Clean interpreter.
    clean_utils = subprocess.run(["make clean"], cwd = INTERPRETER_UTILS_DIR, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    clean_execs = subprocess.run(["make clean"], cwd = INTERPRETER_EXECS_DIR, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    
    if clean_utils.returncode != 0:
        print("Failed to clean interpreter library.")
        sys.exit(1)
    
    if clean_execs.returncode != 0:
        print("Failed to clean interpreter executables.")
        sys.exit(1)


