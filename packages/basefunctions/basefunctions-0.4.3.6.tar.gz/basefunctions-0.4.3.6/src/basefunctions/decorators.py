"""
# =============================================================================
#
#  Licensed Materials, Property of Ralph Vogl, Munich
#
#  Project : basefunctions
#
#  Copyright (c) by Ralph Vogl
#
#  All rights reserved.
#
#  Description:
#
#  simple decorators for multiple purposes
#
# =============================================================================
"""

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
import time

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
# DECORATOR DEFINITIONS
# -------------------------------------------------------------
def logger(func):
    def inner(*args, **kwargs):
        print(f"---> Calling: {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"<--- Return:  {func.__name__} {result} ")
        return result

    return inner


def function_timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # Get the current time as a pandas Timestamp
        result = func(*args, **kwargs)
        end_time = time.perf_counter()  # Get the ending time
        print(f"Runtime of {func.__name__}: {end_time-start_time:.8f} seconds")
        return result

    return wrapper


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def auto_getter(cls):
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)

        # Dynamische Getter für Attribute aus __init__
        for attr, _ in self.__dict__.items():
            if not attr.startswith("_"):
                getter_method = lambda self, a=attr: getattr(self, a)
                setattr(self.__class__, f"get_{attr}", getter_method)

    cls.__init__ = new_init
    return cls

def auto_setter(cls):
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        
        # Dynamische Setter für Attribute aus __init__
        for attr, value in self.__dict__.items():
            if not attr.startswith('_'):
                setter_method = lambda self, val, a=attr: setattr(self, a, val)
                setattr(self.__class__, f'set_{attr}', setter_method)

    cls.__init__ = new_init
    return cls
    