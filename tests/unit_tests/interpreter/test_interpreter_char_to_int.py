# test_interpterer_char_to_int.py - tests interpretation of char->integer
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

INTERPRETER_UTILS_DIR = "./interpreter/utils/"
INTERPRETER_EXECS_DIR = "./interpreter/execs/"
INTERPRET = "./interpreter/execs/interpret"

class CharToIntInterpreterTests(unittest.TestCase):
    """
    Unit testing framework for interpreting (char->integer e).
    """
    def _interpret(self, source: bytes) -> int:
        """
        Calls interpreter and interprets byte code.

        Args:
            source (bytes): Bytecode to be interpreted.

        Returns:
            int: Integer value output by interpreter.
        """
        inter = subprocess.Popen([INTERPRET], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

        stdout, stderr = inter.communicate(source)

        return int(stdout.decode("utf-8"))

    def test_char_to_int_newline(self):
        """
        Test convert newline to 10.
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x0A\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), 10)

    def test_char_to_int_a(self):
        """
        Test convert a to 97.
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x61\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), 97)

if __name__ == '__main__':
    unittest.main()
