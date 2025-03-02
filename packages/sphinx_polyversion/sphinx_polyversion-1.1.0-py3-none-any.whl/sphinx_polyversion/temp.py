from pathlib import Path
from typing import Any, Callable, Iterable
from .pyvenv import Pip

PACKAGE_NAME = "test"


class PipSetuptoolsSCM(Pip):
    def __init__(self, path, name, venv, args, creator=None, temporary=False, env=None):
        env = env or {}
        env[f"SETUPTOOLS_SCM_PRETEND_VERSION_{PACKAGE_NAME}"] = name.lstrip("v")
        super().__init__(
            path, name, venv, args=args, creator=creator, temporary=temporary, env=env
        )
