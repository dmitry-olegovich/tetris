class Counter():
    """DOCSTRING HERE
    """
    
    def __init__(self, max: int = 1000, value: int = 0):
        self._val = value
        self._max = max

    
    def __lt__(self, other):
        if type(other) == int:
            return self._val < other
        if type(other) == Counter:
            return self._val < other._val
        else:
            raise TypeError
    
    def __eq__(self, other):
        if type(other) == int:
            return self._val == other
        if type(other) == Counter:
            return self._val == other._val
        else:
            raise TypeError

    def __gt__(self, other):
        if type(other) == int:
            return self._val > other
        if type(other) == Counter:
            return self._val > other._val
        else:
            raise TypeError

    def checks_out(self):
        if self._val >= self._max:
            return False
        
        return True

    def increment(self):
        self._val += 1

    def reset(self):
        self._val = 0
