# parser.py - 
#
# Josh Meise
# 01-26-2026
# Description: 
#

import subprocess
import ast

PARSER_EXEC = "./parser_exec"

def scheme_parse(source: str) -> list:
    """
    Creates a pipe to write parse string to stdin of Bison parser.
    Bison parser creates AST and writes it to stdout.

    Args:
        source (str): Scheme source program.

    Returns:
        list: Abstract syntax tree in the form of a Python list.

    Raises:
        RuntimeError: Parser fails.
    """
    proc = subprocess.Popen([PARSER_EXEC], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    stdout, stderr = proc.communicate(source.encode("utf-8"))

    if proc.returncode != 0:
        raise RuntimeError("Parsing failed.")
    
    tree = ast.literal_eval(stdout.decode("utf-8"))

    return tree

if __name__ == "__main__":
    print(scheme_parse("20"))
    print(scheme_parse("#t"))
    print(scheme_parse("(+ 2 3)"))
    print(scheme_parse("(add1 (+ 3 4))"))
