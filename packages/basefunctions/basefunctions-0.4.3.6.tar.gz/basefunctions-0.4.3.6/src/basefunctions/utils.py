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
#  a simple module for some helper functions
#
# =============================================================================
"""

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
import inspect

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
# FUNCTION DEFINTIONS
# -------------------------------------------------------------
def get_current_function_name() -> str:
    """
    Get the name of the current function

    Returns
    -------
    str
        name of the current function
    """
    # Get the current stack frame
    frame = inspect.currentframe()
    # Get the function name from the stack frame (2 levels up, since 1 level is this function)
    return inspect.getframeinfo(frame.f_back).function
