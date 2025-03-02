from __future__ import annotations

import os
from abc import abstractmethod, ABC
from typing import Optional

from holytools.logging import Loggable, LogLevel


# ---------------------------------------------------------

class BaseConfigs(Loggable, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._map = {None : {}}
        self._populate_map()

    @abstractmethod
    def _populate_map(self):
        pass

    @staticmethod
    def _as_abspath(path: str) -> str:
        path = os.path.expanduser(path=path)
        path = os.path.abspath(path)
        return path

    # ---------------------------------------------------------
    # interface

    def get(self, key : str, section : Optional[str] = None) -> Optional[str]:
        try:
            config_value = self._map[section][key]
        except KeyError:
            self.log(msg=f'Could not find key \"{key}\" under section \"{section}\" in configs', level=LogLevel.WARNING)
            config_value = None

        return config_value

    def set(self, key : str, value : str, section : Optional[str] = None):
        if not section in self._map:
            self._map[section] = {}
        if key in self._map[section]:
            raise ValueError(f'Key \"{key}\" already exists in settings')

        self._map[section][key] = value
        self._update_resource()

    def remove(self, key : str, section : Optional[str] = None):
        if key in self._map[section]:
            del self._map[section][key]
            self._update_resource()

    def get_general_section(self) -> dict[str, str]:
        return self._map[None]

    @abstractmethod
    def _update_resource(self):
        pass



