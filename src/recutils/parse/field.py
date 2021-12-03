import re

class Field:
    _name_regex = re.compile(
        r"^[a-zA-Z%][a-zA-Z0-9_]*$")

    def __init__(self, name, value):
        if not self._name_regex.match(name):
            raise ValueError("Invalid field name: {}".format(name))
        self._name = name
        self._value = value
        
    def __repr__(self):
        return str(self._value)
        
    @property
    def stdout(self):
        return "{}: {}".format(self._name, self._value)
