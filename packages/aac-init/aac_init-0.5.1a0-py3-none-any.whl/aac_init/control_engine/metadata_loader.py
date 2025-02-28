import json
import os
import threading

from aac_init.log_utils import LazyLogger

logger = LazyLogger("metadata_loader")

class NestedDict:

    def __init__(self, data=None):
        data = data or {}
        for key, value in data.items():
            if isinstance(value, dict):
                value = NestedDict(value)
            self.__dict__[key] = value

    def __getattr__(self, name):
        """Return None for non-existent attributes"""
        return self.__dict__.get(name, None)

    def to_dict(self):
        return {
            key: value.to_dict() if isinstance(value, NestedDict) else value
            for key, value in self.__dict__.items()
        }


class Metadata:
    """Singleton class for managing metadata with dot notation access"""
    _instance = None
    _lock = threading.Lock()
    _RUNTIME_DATA_PATH = "metadata.json"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._data, cls._instance.load_status = cls._load_data()
        return cls._instance

    @classmethod
    def _load_data(cls):
        """Load metadata from JSON file, or raise an error if invalid and set load_status"""
        if os.path.exists(cls._RUNTIME_DATA_PATH):
            with open(cls._RUNTIME_DATA_PATH, "r") as file:
                try:
                    data = json.load(file)
                    return NestedDict(data), True
                except Exception as e:
                    return NestedDict(), False
        return NestedDict(), False

    def save(self):
        """Save metadata to a JSON file"""
        with open(self._RUNTIME_DATA_PATH, "w") as file:
            json.dump(self._data.to_dict(), file, indent=4)
        print(f"Metadata saved to {self._RUNTIME_DATA_PATH}")

    def reset(self):
        """Reset metadata to an empty structure"""
        self._data = NestedDict()
        self.load_status = "failed"  # Reset status to "failed" after reset
        self.save()

    def __getattr__(self, name):
        """Enable dot notation access for metadata and return None if key doesn't exist"""
        return getattr(self._data, name, None)

    def __setattr__(self, name, value):
        if name in {"_data", "_lock", "load_status"}:
            super().__setattr__(name, value)
        else:
            setattr(self._data, name, value)


metadata = Metadata()

