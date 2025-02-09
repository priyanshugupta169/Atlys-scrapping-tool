from abc import ABC, abstractmethod

# The `NotifierInterface` class is an abstract base class in Python with an abstract method `notify`
# that takes a message as a parameter.
class NotifierInterface(ABC):
    @abstractmethod
    def notify(self, message: str):
        pass

# The `ConsoleNotifier` class implements the `notify` method to print a notification message to the
# console.
class ConsoleNotifier(NotifierInterface):
    def notify(self, message: str):
        print(f"[NOTIFICATION]: {message}")
