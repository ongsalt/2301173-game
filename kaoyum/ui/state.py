from typing import TypeVar, Generic, Callable
from random import randint

K = TypeVar("K") 
class Observable(Generic[K]): # an Observable
    def __init__(self, value: K):
        super().__init__()
        self._value = value
        self.callbacks = []

    def subscribe(self, callback: Callable[[K], None]) -> Callable[[], None]:
        """
        Subscribe to the state changes.
        Returns a function to unsubscribe the callback.
        """
        self.callbacks.append(callback)
        return lambda: self.callbacks.remove(callback)
    
    @property
    def value(self) -> K:
        return self._value

    @value.setter
    def value(self, value: K) -> None:
        self._value = value
        for callback in self.callbacks:
            callback(value)

class State: # a State
    def __init__(self):
        self._dirty = True
        self._invalidation_marker = randint(0, 1000000)

    def __setattr__(self, name, value):
        if name not in ["_dirty", "_invalidation_marker"]:
            self._dirty = True
            self._invalidation_marker += 1
        return super().__setattr__(name, value)
    
    # dirty will be set to False when the state is flushed