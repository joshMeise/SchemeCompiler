# utils.py - 
#
# Josh Meise
# 02-18-2026
# Description: 
#

class Free:
    def __init__(self, name):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def __eq__(self, other):
        if not isinstance(other, Free):
            return False
        return self.name == other.name

class Bound:
    def __init__(self, name):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def __eq__(self, other):
        if not isinstance(other, Bound):
            return False
        return self.name == other.name

class Local:
    def __init__(self, name):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def __eq__(self, other):
        if not isinstance(other, Local):
            return False
        return self.name == other.name

