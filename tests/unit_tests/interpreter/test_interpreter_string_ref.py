# test_interpterer_string_ref.py - tests interpretation of string-ref
#
# Josh Meise
# 02-02-2026
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

class StringRefInterpreterTests(unittest.TestCase):
    """
    Unit testing framework for interpreting (string-ref (string "...") e).
    """
    def _interpret(self, source: bytes) -> str:
        """
        Calls interpreter and interprets byte code.

        Args:
            source (bytes): Bytecode to be interpreted.

        Returns:
            str: Value output by interpreter.
        """
        inter = subprocess.Popen([INTERPRET], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

        stdout, stderr = inter.communicate(source)

        if inter.returncode != 0:
            raise RuntimeError("Error in parse.")

        return stdout.decode("utf-8")

    def test_string_ref_regular_1(self):
        """
        Test (string-ref (string "hi") 0).
        """
        self.assertEqual(self._interpret(b"\x1C\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x68\x00\x00\x00\x00\x00\x00\x00\x69\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1D\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), "#\\h\n")

    def test_string_ref_regular_2(self):
        """
        Test (string-ref (string "hi") 1).
        """
        self.assertEqual(self._interpret(b"\x1C\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x68\x00\x00\x00\x00\x00\x00\x00\x69\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x1D\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), "#\\i\n")

    def test_string_ref_invalid_index(self):
        """
        Test (string-ref (string "hi") 2).
        """
        with self.assertRaises(RuntimeError):
            self._interpret(b"\x1C\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x68\x00\x00\x00\x00\x00\x00\x00\x69\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x1D\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

if __name__ == '__main__':
    unittest.main()
