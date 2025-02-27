"""
This module defines the file directory structure
"""

from typing import Optional

from pydantic import Field
from evoml_client.conf.base_default_conf import BaseDefaultConf, conf_factory


# from evoml_api_models import BaseDefaultConf, conf_factory


# ────────────────────────────────────────── imports ────────────────────────────────────────── #
# from thor_file_api.service.conf.base_default_conf import BaseDefaultConf, conf_factory


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                      Data Configuration                                       #
# ───────────────────────────────────────────────────────────────────────────────────────────── #


class ClientConf(BaseDefaultConf):
    """
    Configuration class of a Data.
    """

    USERNAME: Optional[str] = Field(None, env="EVOML_USERNAME")
    PASSWORD: Optional[str] = Field(None, env="EVOML_PASSWORD")
    DOWNLOADS_PATH: Optional[str] = "/tmp/evoml-client"
    BASE_URL: Optional[str] = Field(None, env="BASE_URL")


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                  Data Configuration Factory                                   #
# ───────────────────────────────────────────────────────────────────────────────────────────── #


def client_conf_factory(_env_file: str = ".env", prefix: str = None, defaults: dict = None, **kwargs) -> ClientConf:
    """
    This is a factory generating an DataConf class specific to a service, loading every value from a generic
    .env file storing variables in uppercase with a service prefix.

    example .env:
       PREFIX_DATA_PATH=/tmp/data
       ...
    """
    return conf_factory(config_class=ClientConf, _env_file=_env_file, prefix=prefix, defaults=defaults, **kwargs)
