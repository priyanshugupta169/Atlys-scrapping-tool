import json
from abc import ABC, abstractmethod
from .config import settings

class StorageInterface(ABC):
    @abstractmethod
    def save_data(self, data: list):
        pass

# The `JSONStorage` class implements a method to save a list of data to a JSON file, overwriting any
# existing content.
class JSONStorage(StorageInterface):
    def __init__(self, file_path: str = None):
        self.file_path = file_path or settings.STORAGE_FILE

    def save_data(self, data: list):
        # For simplicity, overwrite with the new scraped data.
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)
