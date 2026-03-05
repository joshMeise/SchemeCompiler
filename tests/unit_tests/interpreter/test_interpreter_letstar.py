# test_interpreter_letstar.py - tests interpreting of let*
#
# Josh Meise
# 03-05-2026
# Description:
#
#

import unittest
import sys
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTERPRET = os.path.join(BASE_DIR, "..", "..", "..", "interpreter", "execs", "interpret")

class LetstarInterpreterTests(unittest.TestCase):
    """
    Unit testing framework for interpreting let*
    """
    def _interpret(self, source: bytes) -> str:
        """
        Calls interpreter and interprets byte code.

        Args:
            source (bytes): Bytecode to be interpreted.

        Returns:
            str: String value output by interpreter.
        """
        inter = subprocess.Popen([INTERPRET], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

        stdout, stderr = inter.communicate(source)

        return stdout.decode("utf-8")

    def test_let_star_simple_1(self):
        """
        Test (letstar ((a 3) (b a) (c b)) c).
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x0C\x00\x00\x00\x00\x00\x00\x00\x16\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x16\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x16\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x17\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), "3\n")

    def test_let_star_simple_1(self):
        """
        Test (letstar ((a 3) (b a) (c a)) c).
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x0C\x00\x00\x00\x00\x00\x00\x00\x16\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x16\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x16\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x17\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), "3\n")


if __name__ == '__main__':
    unittest.main()
