# test_interpterer_char.py - tests character interpretation
#
# Josh Meise
# 01-19-2026
# Description:
#
# Citations:
# - ChatGPT for subprocess with stdin and capturing stdout.
#

import unittest
import sys
import os
import subprocess

INTERPRET = "./interpreter/execs/interpret"

class CharacterInterpreterTests(unittest.TestCase):
    """
    Unit testing framework for interpreting characters.
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

    def test_a(self):
        """
        Test 'a' as a value.
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x61\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), "#\\a\n")

    def test_A(self):
        """
        Test 'A' as a value.
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x41\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), "#\\A\n")

    def test_newline(self):
        """
        Test '\n' as a value.
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x0A\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), "#\\newline\n")

    def test_double_quote(self):
        """
        Test '"' as a value.
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x22\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), "#\\\"\n")

if __name__ == '__main__':
    unittest.main()
