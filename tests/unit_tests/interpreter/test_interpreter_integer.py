# test_interpterer_integer.py - tests integer interpretation
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

class IntegerInterpreterTests(unittest.TestCase):
    """
    Unit testing framework for interpreting integers.
    """

    def _interpret(self, source: bytes) -> int:
        """
        Calls interpreter and interprets byte code.

        Args:
            source (bytes): Bytecode to be interpreted.

        Returns:
            int: Integer value output by interpreter.
        """
        make_utils = subprocess.run(["make clean; make"], cwd = INTERPRETER_UTILS_DIR, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
        make_execs = subprocess.run(["make clean; make"], cwd = INTERPRETER_EXECS_DIR, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    
        if make_utils.returncode != 0:
            print("Failed to build interpreter library.")
    
        if make_execs.returncode != 0:
            print("Failed to build interpreter executables.")

        inter = subprocess.Popen([INTERPRET], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

        stdout, stderr = inter.communicate(source)

        # Clean interpreter.
        clean_utils = subprocess.run(["make clean"], cwd = INTERPRETER_UTILS_DIR, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
        clean_execs = subprocess.run(["make clean"], cwd = INTERPRETER_EXECS_DIR, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    
        if clean_utils.returncode != 0:
            print("Failed to clean interpreter library.")
    
        if clean_execs.returncode != 0:
            print("Failed to clean interpreter executables.")

        return int(stdout)

    def test_pass_4(self):
        """
        Test valid integer value of 4.
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), 4)

    def test_pass_1(self):
        """
        Test valid integer value of 1.
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), 1)

    def test_pass_0(self):
        """
        Test valid integer value of 4.
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), 0)



if __name__ == '__main__':
    unittest.main()
