import os
import threading
from pathlib import Path

import yaml

from hub.schema.app_schema import AppSchema


class AppSetting(object):
    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls, filepath: Path):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls, filepath)
        else:
            cls._instance.initial_config(filepath)
        return cls._instance

    def __init__(self, filepath: Path):
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self.filepath = filepath
                    self._config = None
                    self.initial_config(filepath)
                    self._initialized = True

    @staticmethod
    def _load_config( filepath):
        if not filepath or not os.path.exists(filepath):
            raise FileNotFoundError(f"File path is None or not found: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def initial_config(self, filepath: Path):
        self.filepath = filepath
        self._config = None
        raw_config = self._load_config(filepath)
        self._config = AppSchema(**raw_config)