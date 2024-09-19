import random

class Die:
    def __init__(self) -> None:
        self._pips = None
        self._is_locked = False
    
    @property
    def pips(self) -> int|None:
        return self._pips
    
    @property
    def is_locked(self) -> bool:
        return self._is_locked

    def roll(self) -> None:
        if not self.is_locked:
            self._pips = random.randint(1, 6)
    
    def toggle_lock(self) -> None:
        self._is_locked = not self._is_locked
    
    def display(self) -> list[str]:
        rows: list[str] = [' _____ ']
        
        if self.pips == 1:
            rows.append('|     |')
        elif self.pips in [2, 3]:
            rows.append('|*    |')
        else:
            rows.append('|*   *|')
        
        if self.pips in [1, 3, 5]:
            rows.append('|  *  |')
        elif self.pips in [2, 4]:
            rows.append('|     |')
        else:
            rows.append('|*   *|')
        
        if self.pips == 1:
            rows.append('|     |')
        elif self.pips in [2, 3]:
            rows.append('|    *|')
        else:
            rows.append('|*   *|')
        
        rows.append(' \u203E\u203E\u203E\u203E\u203E ')

        return rows
