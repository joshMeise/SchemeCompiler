# compile.py - 
#
# Josh Meise
# 01-10-2026
# Description: 
#

import sys
import os
sys.path.append(os.path.abspath("./compiler"))
from compiler.compiler import Compiler
from parser import *

ARGC = [1, 2, 3]

def compile_program(input: StringIO, output: BinaryIO):
    """
    Compiles a Scheme program and writes bytecode to output file.

    Args:
        input (StringIO): Scheme source code.
        output (BinaryIO): Binary file to write bytecode to.
    """
    source = input.read()
    program = scheme_parse(source)
    compiler = Compiler()
    compiler.compile_function(program)
    compiler.write_to_stream(output)

if __name__ == "__main__":
    # Parse arguments.
    if len(sys.argv) not in ARGC:
        print("usage: python3 compile.py [ input_file.scm ] [ output_file.bc ]")
        sys.exit(1)

    # Set input to stdin and output to stdout.
    if len(sys.argv) == 1:
        input = sys.stdin
        output = sys.stdout.buffer
        compile_program(input, output)
    # Open files.
    elif len(sys.argv) == 3:
        with open(sys.argv[1], "rb") as input, open(sys.argv[2], "wb") as output:
            compile_program(input, output)
    # Check which argument was provided and open respctive files.
    elif len(sys.argv[1]) > 2 and sys.argv[1][-3:] == ".bc":
        input = sys.stdin
        with open(sys.argv[1], "wb") as output:
            compile_program(input, output)
    elif len(sys.argv[1]) > 3 and sys.argv[1][-3:] == ".scm":
        output = sys.stdout.buffer
        with open(sys.argv[1], "rb") as intput:
            compile_program(input, output)
    else:
        print("usage: python3 compile.py [ input_file.scm ] [ output_file.bc ]")
        sys.exit(1)
