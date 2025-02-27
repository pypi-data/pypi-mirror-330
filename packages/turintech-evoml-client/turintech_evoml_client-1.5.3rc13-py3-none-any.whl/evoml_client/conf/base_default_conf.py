"""
This module contains a base configuration class that takes the values of the environment variables and
allows setting different default values to those implemented in the configuration class.
"""

# ────────────────────────────────────────── imports ────────────────────────────────────────── #
from pydantic import BaseSettings


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                               Base Configuration with Defaults                                #
# ───────────────────────────────────────────────────────────────────────────────────────────── #


class BaseDefaultConf(BaseSettings):
    """
    Base class for settings, allowing values to be overridden by environment variables.

    Field value priority
        In the case where a value is specified for the same Settings field in multiple ways,
        the selected value is determined as follows (in descending order of priority):
            1. Arguments passed to the Settings class initializer.
            2. Environment variables, e.g. my_prefix_special_function.
            3. Variables loaded from a dotenv (.env) file.
            4. Variables loaded from the secrets directory.
            5. Variables loaded from the 'defaults' argument
            6. The default field values for the Settings model.
    """

    def __init__(self, _env_file: str = ".env", defaults: dict = None, **values):
        # Update the default field values for the Settings model with the new values
        self._update_defaults(defaults=defaults or {})

        # Arguments passed to the Settings class initializer and Environment variables
        super().__init__(_env_file=_env_file, **values)

        # Initialize None attributes with class defaults
        self._update_empty_values()

    def _update_defaults(self, defaults: dict):
        """
        Updating the default values of the attributes
        """
        for key, value in defaults.items():
            if key in self.__fields__:
                entry = self.__fields__.get(key)
                entry.default = value
                entry.required = False
                self.__fields__[key] = entry

    def _update_empty_values(self):
        """
        Updating the attributes for which its value has not been indicated through the environment variables.
        """


# ───────────────────────────────────────────────────────────────────────────────────────────── #
#                                     Configuration Factory                                     #
# ───────────────────────────────────────────────────────────────────────────────────────────── #


def conf_factory(
    config_class,
    _env_file: str = ".env",
    prefix: str = None,
    defaults: dict = None,
    **kwargs,
):
    """
    This is a factory generating an 'config_class' class specific to a service, loading every value from a generic
    .env file storing variables in uppercase with a service prefix.

    :param config_class: (Callable[..., BaseModel]) Class type inheriting from BaseModel to instantiate.
    :param _env_file: Configuration file of the environment variables from where to load the values.
    :param prefix: Prefix that the class attributes must have in the environment variables.
    :param defaults: New values to override the default field values for the configuration model.
    :param kwargs: Arguments passed to the Settings class initializer.

    :return: Object of the required configuration class
    """

    class ConfFactory(config_class):
        """Configuration Class Factory"""

        class Config(config_class.Config):
            """Class with base attributes for configuration"""

            env_prefix = f"{prefix}_" if prefix else ""

    return ConfFactory(_env_file=_env_file, defaults=defaults, **kwargs)
