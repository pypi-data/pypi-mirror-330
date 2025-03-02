# config.py
from .constants import DEFAULT_CONFIG

class Config:
    def __init__(self):
        self._config = DEFAULT_CONFIG.copy()  # Copy to prevent accidental modification of defaults

    def set(self, key, value):
        if key in self._config:
            self._config[key] = value
        else:
            raise KeyError(f"{key} is not a configurable constant.")

    def get(self, key):
        return self._config.get(key, None)

# Global instance for easy access
config = Config()