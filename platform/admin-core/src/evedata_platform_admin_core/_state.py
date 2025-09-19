from evedata_platform_core import Configuration
from rich.console import Console


class AdminState:
    _config: Configuration
    _out: Console
    _err: Console

    def __init__(self):
        self._config = Configuration()
        self._out = Console()
        self._err = Console(stderr=True)

    @property
    def config(self) -> Configuration:
        return self._config

    @property
    def out(self) -> Console:
        return self._out

    @property
    def err(self) -> Console:
        return self._err
