# test_interpterer_int_to_char.py - tests interpretation of integer->char
#
# Josh Meise
# 01-09-2026
# Description:
#
# Citations:
# - ChatGPT for subprocess with stdin and capturing stdout.
#

import unittest
import sys
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTERPRET = os.path.join(BASE_DIR, "..", "..", "..", "interpreter", "execs", "interpret")

class IntToCharInterpreterTests(unittest.TestCase):
    """
    Unit testing framework for interpreting (integer->char e).
    """
    def _interpret(self, source: bytes) -> str:
        """
        Calls interpreter and interprets byte code.

        Args:
            source (bytes): Bytecode to be interpreted.

        Returns:
            str: string output by the interpreter
        """
        inter = subprocess.Popen([INTERPRET], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

        stdout, stderr = inter.communicate(source)

        return stdout.decode("utf-8")

    def test_int_to_char_regular(self):
        """
        Test (integer->char 97).
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x84\x01\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), "#\\a\n")

if __name__ == '__main__':
    unittest.main()
