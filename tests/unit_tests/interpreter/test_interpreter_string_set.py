# test_interpterer_string_set.py - tests interpretation of string-set
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

class StringSetInterpreterTests(unittest.TestCase):
    """
    Unit testing framework for interpreting (string-set! (string "...") e e).
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

    def test_string_set_regular_1(self):
        """
        Test (string-set! (string "hi") 0 a).
        """
        self.assertEqual(self._interpret(b"\x1C\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x68\x00\x00\x00\x00\x00\x00\x00\x69\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x61\x00\x00\x00\x00\x00\x00\x1E\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), "\"ai\"\n")

    def test_string_set_regular_2(self):
        """
        Test (string-set! (string "hi") 1 b).
        """
        self.assertEqual(self._interpret(b"\x1C\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x68\x00\x00\x00\x00\x00\x00\x00\x69\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x62\x00\x00\x00\x00\x00\x00\x1E\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), "\"hb\"\n")

    def test_string_set_invalid_index(self):
        """
        Test (string-set! (string "hi") 2 b).
        """
        with self.assertRaises(RuntimeError):
            self._interpret(b"\x1C\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x68\x00\x00\x00\x00\x00\x00\x00\x69\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x62\x00\x00\x00\x00\x00\x00\x1E\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

if __name__ == '__main__':
    unittest.main()
