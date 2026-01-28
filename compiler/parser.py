# parser.py - 
#
# Josh Meise
# 01-26-2026
# Description: 
#
# Citations:
# - ChatGPT for help using __file__ to allow running this program from any directory.
#

import subprocess
import ast
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARSER_EXEC = os.path.join(BASE_DIR, "parser", "execs", "parser_exec")

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
