"""Configuration utilities.

src/utils/config.py

The purpose of this module is to provide a typesafe way of managing
the configuration of the application. Configuration is pulled from
environment variables and/or a .env file. The configuration is then
stored as environment variables.

NOTE: Environment variables take precedence over .env file variables.
Any variables defined in the .env file will be overwritten by the
environment variables.
"""

import os
import dotenv
import json
import pathlib

from typing import TypeVar, Any

T = TypeVar("T")


def get_config_variable(
    name: str, var_type: T, default: T, required: bool = False
) -> Any:
    """Get a configuration variable.

    If the variable is not defined, the default value will be returned.
    """
    variable = os.getenv(name)
    if variable is None:
        dotenv_vars = dotenv.dotenv_values()
        variable = dotenv_vars[name] if name in dotenv_vars else None

    if variable is None:
        if required:
            raise ValueError(f"Required variable {name} not defined!")
        else:
            return default

    variable = str(variable)
    if var_type == str:
        return variable  # type: ignore

    parsed = json.loads(variable)
    if not isinstance(parsed, var_type):  # type: ignore
        raise TypeError(f"Variable {name} is not of type {var_type}!")
    return parsed


class Config:
    """Configuration schema.

    Provides a way to define the configuration schema of the application.
    """

    db_user: str = get_config_variable("DB_USER", str, "", required=True)
    db_password: str = get_config_variable("DB_PASSWORD", str, "", required=True)
    db_host: str = get_config_variable("DB_HOST", str, "127.0.0.1")
    db_port: int = get_config_variable("DB_PORT", int, 3306)
    db_database: str = get_config_variable("DB_DATABASE", str, "", required=True)

    product_config_path: str = get_config_variable(
        "PRODUCT_CONFIG_PATH", str, "./products.yml"
    )
    
    root_admin_username: str = get_config_variable("ROOT_ADMIN_USERNAME", str, "", required=True)
    root_admin_password: str = get_config_variable("ROOT_ADMIN_PASSWORD", str, "", required=True)

    @staticmethod
    def get_database_connection_string() -> str:
        """Get the database connection string."""
        return f"mysql+pymysql://{Config.db_user}:{Config.db_password}@{Config.db_host}:{Config.db_port}/{Config.db_database}"
