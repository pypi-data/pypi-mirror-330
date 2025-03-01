"""
=============================================================================

  Licensed Materials, Property of Ralph Vogl, Munich

  Project : backtraderfunctions

  Copyright (c) by Ralph Vogl

  All rights reserved.

  Description:

  a simple config handler for reading configurations from YAML files

=============================================================================
"""

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
from typing import Any
import basefunctions
import os
import yaml

# -------------------------------------------------------------
#  FUNCTION DEFINITIONS
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS REGISTRY
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------
DEFAULT_PATHNAME = ".config"

# -------------------------------------------------------------
# VARIABLE DEFINTIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
# CLASS DEFINITIONS
# -------------------------------------------------------------
@basefunctions.singleton
class ConfigHandler:
    """
    The ConfigHandler class is a singleton designed to handle and
    abstract configuration management. It reads configurations from
    YAML files and stores them in a dictionary, allowing access by
    package name and configuration element name.

    Configurations are stored in a YAML file format, with the
    package name as the filename.

    Example:
    ```
    config_handler.ConfigHandler().load_config("configs/config.yaml")
    ```
    """

    def __init__(self):
        self.config = {}  # Dictionary to store configurations

    def load_config(self, file_path: str) -> None:
        """
        Load a YAML configuration file into the configs dictionary.

        Parameters:
        -----------
            file_path: str
                Path to the YAML configuration file.

        Raises:
        -------
            FileNotFoundError: If the specified file does not exist.
            yaml.YAMLError: If there is an error in parsing the YAML file.
            ValueError: If the YAML file is empty or invalid.
            RuntimeError: If there is an unexpected error.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file) or {}  # Use an empty dict if the file is empty
                self.config.update(config)
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"File not found: '{file_path}'") from exc
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file at '{file_path}': {e}")
        except Exception as exc:
            raise RuntimeError(f"Unexpected error: {exc}") from exc

    def load_default_config(self, package_name: str) -> None:
        """
        Load the default configuration for a given package.

        Parameters:
        -----------
            package_name: str
                The name of the package to load the default configuration for.

        Raises:
        -------
            FileNotFoundError: If the default configuration file does not exist.
        """
        file_name = os.path.join(
            basefunctions.get_home_path(), DEFAULT_PATHNAME, package_name, f"{package_name}.yaml"
        )
        if not basefunctions.check_if_file_exists(file_name):
            self.create_default_config(package_name)
        self.load_config(file_name)

    def create_default_config(self, package_name: str) -> None:
        """
        Create a default configuration file for a given package.

        Parameters:
        -----------
            package_name: str
                The name of the package to create the default configuration for.

        Raises:
        -------
            ValueError: If the package name is not provided.
        """
        if not package_name:
            raise ValueError("Package name must be provided.")

        config_directory = os.path.join(
            basefunctions.get_home_path(), DEFAULT_PATHNAME, package_name
        )
        basefunctions.create_directory(config_directory)

        with open(
            os.path.join(config_directory, f"{package_name}.yaml"), "w", encoding="utf-8"
        ) as file:
            yaml.dump({package_name: None}, file)

    def get_config(self, package=None):
        """
        Get the config for a specific package
        """
        return self.config if package is None else self.config.get(package, {})

    def get_config_value(self, path: str, default_value: Any = None) -> Any:
        """
        Retrieve the value of a configuration element by its path.

        Parameters:
        -----------
            path: str
                The path to the configuration element.
            default_value: Any
                The default value to return if the path is not found.

        Returns:
        --------
            Any
                The value of the configuration element or default_value if not found.
        """
        keys = path.split("/")
        value = self.config

        for key in keys:
            value = value.get(key, default_value)
            if value is default_value:
                return default_value

        return value
