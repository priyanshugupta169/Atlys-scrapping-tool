# The `CacheManager` class provides methods to get and set key-value pairs in a cache dictionary.
class CacheManager:
    def __init__(self):
        self.cache = {}

    def get(self, key: str):
        return self.cache.get(key)

    def set(self, key: str, value: dict):
        self.cache[key] = value
