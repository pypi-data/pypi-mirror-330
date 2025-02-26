"""
This module implements and instantiates the common configuration class used in the project.
"""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Type

# Internal libraries
from core_common_configuration.base_conf_env import BaseConfEnv, BaseConfEnvT, conf_factory
from core_common_data_types.type_definitions import PathType

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["BaseConfManager"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                Configuration Manager                                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class BaseConfManager:
    """
    Configuration Manager class.
    """

    # Environment file
    _path_env_file: Optional[Path] = None
    _env_file: Optional[str] = None

    # Main config map
    _config_map: Dict[str, BaseConfEnv]

    def __init__(self, env_file: Optional[PathType] = None):
        self._env_file, self._path_env_file = self._retrieve_environment_file(env_file=env_file)

        self._config_map = {}

    # --------------------------------------------------------------------------------------------------

    @property
    def env_file(self) -> str:
        """
        Environment configuration file used in the current configuration.
        """
        return self._env_file or ""

    def _retrieve_environment_file(self, env_file: Optional[PathType] = None) -> Tuple[Optional[str], Optional[Path]]:
        return (str(env_file), Path(env_file)) if env_file and Path(env_file).exists() else (None, None)

    # --------------------------------------------------------------------------------------------------

    def get_conf(
        self,
        conf_type: Type[BaseConfEnvT],
        conf_name: str,
        prefix: Optional[str] = None,
        defaults: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> BaseConfEnvT:
        if conf_name not in self._config_map:
            self.update_conf(conf_type=conf_type, conf_name=conf_name, prefix=prefix, defaults=defaults, **kwargs)
        elif not isinstance(self._config_map[conf_name], conf_type):
            raise ValueError(
                f"Config error: '{conf_name}' config structure is not compatible with {conf_type.__name__}"
            )
        # TODO: https://github.com/python/mypy/issues/10003
        return self._config_map[conf_name]  # type: ignore[return-value]

    def update_conf(
        self,
        conf_type: Type[BaseConfEnvT],
        conf_name: str,
        prefix: Optional[str] = None,
        defaults: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> BaseConfEnvT:
        conf = conf_factory(config_class=conf_type, _env_file=self.env_file, prefix=prefix, defaults=defaults, **kwargs)
        self._config_map[conf_name] = conf
        return conf

    def reset_conf(self, conf_name: str):
        self._config_map.pop(conf_name, None)
