class Counter():
    """A simple counter class used as timer.
    
    Args:
        max (int): maximum value at which counter will need to be reset.
        value (int): initial value if it needs to be > 0
    
    Attributes:
        _val = current counter value
        _max = at this value Counter.checks_out() will start returning
            False value
    """
    
    def __init__(self, max: int = 1000, value: int = 0):
        self._val = value
        self._max = max
        self._checkpoint = 0

    
    def __lt__(self, other):
        """< defined for int and Counter."""

        if type(other) == int:
            return self._val < other
        if type(other) == Counter:
            return self._val < other._val
        else:
            raise TypeError
    
    def __eq__(self, other):
        """== defined for int and Counter."""

        if type(other) == int:
            return self._val == other
        if type(other) == Counter:
            return self._val == other._val
        else:
            raise TypeError

    def __gt__(self, other):
        """> defined for int and Counter."""

        if type(other) == int:
            return self._val > other
        if type(other) == Counter:
            return self._val > other._val
        else:
            raise TypeError

    def checks_out(self):
        """Return True if counter value < max."""
        
        if self._val >= self._max:
            return False
        
        return True

    def increment(self):
        self._val += 1

    def reset(self):
        self._val = 0

    def sub_timer(self, value):
        if not self._checkpoint:
            self._checkpoint = self._val - 1
        result = self._val - self._checkpoint % value
        if not result:
            self._checkpoint = 0
        return bool(result)
