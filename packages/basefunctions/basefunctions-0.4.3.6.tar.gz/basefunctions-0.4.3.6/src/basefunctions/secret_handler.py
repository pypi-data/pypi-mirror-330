"""
# =============================================================================
#
#  Licensed Materials, Property of Ralph Vogl, Munich
#
#  Project : stocksdatabase
#
#  Copyright (c) by Ralph Vogl
#
#  All rights reserved.
#
#  Description:
#
#  a simple module to keep secrets private
#
# =============================================================================
"""

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
from typing import Any
import basefunctions
import os
import load_dotenv

# -------------------------------------------------------------
#  FUNCTION DEFINITIONS
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS REGISTRY
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------

# -------------------------------------------------------------
# VARIABLE DEFINTIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
# CLASS DEFINTIONS
# -------------------------------------------------------------


@basefunctions.singleton
class SecretHandler:
    """
    class SecretHandler loads .env file in home directory and makes all values available
    via get_secret_value method
    """

    config = None

    def __init__(self):
        """
        Constructor of SecretHandler class, reads the .env file in home directory
        as the standard config file and makes all values available
        """
        env_filename = f"{os.path.expanduser('~')}{os.path.sep}.env"
        load_dotenv.load_dotenv(env_filename)

    def get_secret_value(self, key: str, default_value: Any = None) -> Any:
        """
        Summary:
        get the secret key from the settings.ini file

        Parameters:
        ----------
        key : str
            the key to get the secret for
        section : str
            the section in the config file
        default_value : Any
            the default value to return if the key is not found

        Returns:
        -------
        Any
            the secret key or the default value
        """
        val = os.getenv(key)
        if not val:
            return default_value
        return val
