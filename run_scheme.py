# run_scheme.py - compiles and interprets a Scehme program
#
# Josh Meise
# 01-18-2026
# Description: 
# - Takes optional input of a Scheme program file to compile and interpret.
# - Takes optonal output of a test file to which to write output of Scheme program.
# - Builds and cleans interpreter.
#
# Citations:
# - ChatGPT and python docs for help with subprocess.
#

import sys
import subprocess
from io import StringIO

ARGC = [1, 2, 3]
INTERPRETER_UTILS_DIR = "./interpreter/utils/"
INTERPRETER_EXECS_DIR = "./interpreter/execs/"

if __name__ == "__main__":
    ret_code = 0

    # Parse arguments.
    if len(sys.argv) not in ARGC:
        print("usage: python3 run_scheme.py [ input_file.scm ] [ output_file.txt ]")
        sys.exit(1)

    # Build interpreter.
    subprocess.run(["make clean; make"], cwd = INTERPRETER_UTILS_DIR, check = True, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    subprocess.run(["make clean; make"], cwd = INTERPRETER_EXECS_DIR, check = True, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

    # Compile with no input (uses stdin) and interpret with no output (uses stdout).
    if len(sys.argv) == 1:
        # Open pipe between compiler and interpreter.
        p1 = subprocess.Popen(["python3", "compiler/compile.py"], stdout = subprocess.PIPE)
        p2 = subprocess.Popen(["./interpreter/execs/interpret"], stdin = p1.stdout)

        p1.stdout.close()
        p2.wait()
        p1.wait()

        # Capture return codes to indicate successful termination.
        if p1.returncode != 0:
            print("Compilation failed.")
            ret_code = 1
        
        if p2.returncode != 0:
            print("Interpretation failed.")
            ret_code = 1

    # Provide arguments to compiler and/or interpreter.
    elif len(sys.argv) == 3:
        # Open pipe between compiler and interpreter.
        p1 = subprocess.Popen(["python3", "compiler/compile.py", sys.argv[1]], stdout = subprocess.PIPE)
        p2 = subprocess.Popen(["./interpreter/execs/interpret", sys.argv[2]], stdin = p1.stdout)
    
        p1.stdout.close()
        p2.wait()
        p1.wait()
    
        # Capture return codes to indicate successful termination.
        if p1.returncode != 0:
            print("Compilation failed.")
            ret_code = 1
            
        if p2.returncode != 0:
            print("Interpretation failed.")
            ret_code = 1

    # Check which argument was provided and open respctive files.
    elif len(sys.argv[1]) > 2 and sys.argv[1][-3:] == ".txt":
        # Open pipe between compiler and interpreter.
        p1 = subprocess.Popen(["python3", "compiler/compile.py"], stdout = subprocess.PIPE)
        p2 = subprocess.Popen(["./interpreter/execs/interpret", sys.argv[1]], stdin = p1.stdout)
    
        p1.stdout.close()
        p2.wait()
        p1.wait()
    
        # Capture return codes to indicate successful termination.
        if p1.returncode != 0:
            print("Compilation failed.")
            ret_code = 1
            
        if p2.returncode != 0:
            print("Interpretation failed.")
            ret_code = 1

    elif len(sys.argv[1]) > 3 and sys.argv[1][-4:] == ".scm":
        # Open pipe between compiler and interpreter.
        p1 = subprocess.Popen(["python3", "compiler/compile.py", sys.argv[1]], stdout = subprocess.PIPE)
        p2 = subprocess.Popen(["./interpreter/execs/interpret"], stdin = p1.stdout)
    
        p1.stdout.close()
        p2.wait()
        p1.wait()
    
        # Capture return codes to indicate successful termination.
        if p1.returncode != 0:
            print("Compilation failed.")
            ret_code = 1
            
        if p2.returncode != 0:
            print("Interpretation failed.")
            ret_code = 1

    else:
        print("usage: python3 run_scheme.py [ input_file.scm ] [ output_file.txt ]")
        ret_code = 1

    # Clean up interpreter.
    subprocess.run(["make clean"], cwd = INTERPRETER_UTILS_DIR, check = True, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    subprocess.run(["make clean"], cwd = INTERPRETER_EXECS_DIR, check = True, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    
    # Exit with apprpriate return code.
    sys.exit(ret_code)
