from typing import TypeVar, Generic, Callable

K = TypeVar("K") 
class State(Generic[K]): # an Observable
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
