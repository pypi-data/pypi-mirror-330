"""
This module implements and instantiates the common configuration class used
in the project.
"""

# ────────────────────────────────── Imports ───────────────────────────────── #
import inspect
import tempfile
from logging import Logger
from pathlib import Path
from typing import Optional, Dict

from core_logging.logger_conf import logger_conf_factory, LoggerConf

from evoml_client.conf.client_conf import ClientConf, client_conf_factory


# ──────────────────────────────────────────────────────────────────────────── #
#                              Configuration Manager                           #
# ──────────────────────────────────────────────────────────────────────────── #


class ConfManager:
    """Configuration Manager class"""

    # APP paths
    path_conf: Path = Path(__file__).parent.resolve()  # conf package
    path_app: Path = path_conf.parent.resolve()  # evoml_client package
    path_src: Path = path_app.parent.resolve()  # src package
    path_root: Path = path_src.parent.resolve()  # evoml-client project

    # APP environment file
    _path_env_file: Path = path_root.joinpath(".env")
    _env_file: str = str(_path_env_file)

    _conf_prefix: str = None

    tmp_directory: Path = Path(tempfile.gettempdir()).joinpath("evoml-client")

    # The Logging Configurations object is instantiated once its use is invoked
    _logging_conf: LoggerConf = None
    defaults_logging_conf: Dict = dict(
        logging_dir=tmp_directory.joinpath("logs"),
        logging_file_name="evoml_client",
    )

    _client_conf: ClientConf = None
    # ──────────────────────────────────────────────────────────────────────── #

    def __init__(self, env_file: str or Path = None):
        if env_file:
            self.update_conf_mgr(env_file=env_file)

    # ──────────────────────────────────────────────────────────────────────── #

    @property
    def env_file(self) -> str:
        """
        Environment configuration file used in the current configuration
        """
        return self._env_file

    def update_conf_mgr(self, env_file: str):
        """
        Update all the configuration by loading the environment variables from the indicated file.
        """
        self._path_env_file = Path(env_file)
        self._env_file = str(self._path_env_file) if self._path_env_file.exists() else None

        if not self._path_env_file.exists():
            print(f"[WARNING] environment file does not exist: {env_file}")
            return

        if self._logging_conf:
            self.update_logging_conf(_env_file=self._env_file)

    @property
    def client_conf(self) -> ClientConf:
        """
        :return: Redis related configuration.
        """
        if self._client_conf is None:
            self.update_client_conf()
        return self._client_conf

    def update_client_conf(self, _env_file: str = None, defaults: dict = None):
        """
        Update the Redis configuration by loading the environment variables from the indicated file and
        taking into account the default values
        """
        factory_args = dict(
            _env_file=_env_file or self._env_file,
        )

        self._client_conf = client_conf_factory(**factory_args)

    # ─────────────────────────────── Logging Utils ────────────────────────────── #

    @property
    def logger(self):
        """Returns the log object of the class"""
        return self.get_logger(
            package_name=__name__,
            class_name=self.__class__.__name__,
            method_name=inspect.stack()[1][3],
        )

    @property
    def logging_conf(self) -> LoggerConf:
        """
        :return: Logging configuration
        """
        if self._logging_conf is None:
            self.update_logging_conf()
        return self._logging_conf

    def update_logging_conf(self, _env_file: str = None, defaults: dict = None):
        """
        Update the LoggingConf configuration by loading the environment
        variables from the indicated file and taking into account default values
        """
        self._logging_conf = logger_conf_factory(
            _env_file=_env_file or self._env_file,
            prefix=self._conf_prefix,
            defaults=defaults or self.defaults_logging_conf,
        )

    def get_package_name(self, file_path: str, src_path: str = path_src) -> Optional[str]:
        """
        :param file_path: "/<root>/<root_project>/<src_path>/<directory>/<subdirectory>/file.py"
        :param src_path: "/<root>/<root_project>/<src_path>/"
        :return: "<directory>.<subdirectory>"
        """
        _src_parts = Path(src_path).parts if src_path else self.path_src.parts
        return (
            None
            if not file_path
            else (
                ".".join(Path(file_path).resolve().relative_to(*_src_parts).parent.parts)
                if _src_parts
                else Path(file_path).parent.parts[-1]
            )
        )

    @staticmethod
    def get_class_name(file_path: str) -> Optional[str]:
        """
        :param file_path: "/<root>/<root_project>/<src_path>/<directory>/<subdirectory>/file.py"
        :return: "<file>"
        """
        if not file_path:
            return None
        return str(Path(file_path).stem)

    def get_logger(
        self,
        file_name: str = None,
        class_name: str = None,
        package_name: str = None,
        method_name: bool or str = None,
        debug=None,
        level: str = None,
        src_path: str = path_src,
    ) -> Logger:
        """
        Return a logger with the specified name, creating it if necessary.

        :param file_name: Python file (__file__) in which the logger will be used.
        :param class_name: Name of the class (self.__class__.__name__) or python file (__file__)
            in which the logger will be used.
        :param package_name: Package name in which the logger will be used (__name__)
        :param method_name: Name of the specific method in which the logger will be used.
            If the indicated value is "True", this value will take the name of the method that invokes this method.
        :param debug: Flag indicating if you want to configure the logger with the DEBUG level
        :param level: Log level
        :param src_path: "/<root>/<root_project>/<src_path>/"

        :return: The logger with name:
            <package_name>.<class_name>.<method_name>
        """

        package_name = package_name or self.get_package_name(file_path=file_name, src_path=src_path)
        class_name = class_name or self.get_class_name(file_path=file_name)
        method_name = inspect.stack()[1][3] if method_name is True else method_name if method_name else None
        return self.logging_conf.get_logger(
            package_name=package_name,
            class_name=class_name,
            method_name=method_name,
            level=level if level is not None else "DEBUG" if debug else None,
        )


# ──────────────────────────────────────────────────────────────────────────────
# ─── ConfManager instance
# ──────────────────────────────────────────────────────────────────────────────

conf_mgr = ConfManager()
