# test_interpterer_times.py - tests interpretation of (* e1 e2 ...)
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

class TimesInterpreterTests(unittest.TestCase):
    """
    Unit testing framework for interpreting (* e1 e2 ..).
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

    def test_times_1_arg(self):
        """
        Test (* 2).
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x0d\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), 2)

    def test_times_2_args(self):
        """
        Test (* 2 3).
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x0C\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x0d\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), 6)

    def test_times_3_args(self):
        """
        Test (* 2 3 4).
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0C\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x0D\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), 24)

if __name__ == '__main__':
    unittest.main()
