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
#  simple library to have some commonly used functions for everyday purpose
#
# =============================================================================

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------

from basefunctions.decorators import logger, function_timer, singleton, auto_getter, auto_setter
from basefunctions.config_handler import ConfigHandler
from basefunctions.filefunctions import (
    check_if_dir_exists,
    check_if_exists,
    check_if_file_exists,
    create_directory,
    create_file_list,
    get_base_name,
    get_base_name_prefix,
    get_current_directory,
    get_extension,
    get_file_extension,
    get_file_name,
    get_parent_path_name,
    get_path_and_base_name_prefix,
    get_path_name,
    get_home_path,
    is_directory,
    is_file,
    norm_path,
    remove_directory,
    remove_file,
    rename_file,
    set_current_directory,
)
from basefunctions.observer import Observer, Subject
from basefunctions.secret_handler import SecretHandler
from basefunctions.threadpool import (
    ThreadPoolMessage,
    ThreadPoolHookObjectInterface,
    ThreadPoolUserObjectInterface,
    create_threadpool_message,
    ThreadPool,
)

from basefunctions.database_handler import (
    DataBaseHandler,
    SQLiteDataBaseHandler,
    MySQLDataBaseHandler,
    PostgreSQLDataBaseHandler,
)

from basefunctions.utils import get_current_function_name


__all__ = [
    "ThreadPool",
    "ThreadPoolMessage",
    "ThreadPoolHookObjectInterface",
    "ThreadPoolUserObjectInterface",
    "auto_getter",
    "auto_setter",
    "check_if_dir_exists",
    "check_if_exists",
    "check_if_file_exists",
    "check_if_table_exists",
    "connect_to_database",
    "create_database",
    "create_directory",
    "create_file_list",
    "create_threadpool_message",
    "execute_sql_command",
    "function_timer",
    "get_base_name",
    "get_base_name_prefix",
    "get_current_directory",
    "get_current_function_name",
    "get_default_threadpool",
    "get_extension",
    "get_file_extension",
    "get_file_name",
    "get_number_of_elements_in_table",
    "get_parent_path_name",
    "get_path_name",
    "get_path_and_base_name_prefix",
    "get_home_path",
    "is_directory",
    "is_file",
    "logger",
    "norm_path",
    "remove_directory",
    "remove_file",
    "rename_file",
    "set_current_directory",
    "singleton",
    "Observer",
    "Subject",
    "ConfigHandler",
    "DataBaseHandler",
    "SQLiteDataBaseHandler",
    "MySQLDataBaseHandler",
    "PostgreSQLDataBaseHandler",
    "SecretHandler",
]

# load default config
ConfigHandler().load_default_config("basefunctions")


def get_default_threadpool() -> ThreadPool:
    """
    returns the default threadpool

    Returns:
    --------
    ThreadPool: the default threadpool
    """
    return default_threadpool


# create a default thread pool, this should be used from all other modules
default_threadpool = ThreadPool(
    num_of_threads=ConfigHandler().get_config_value(
        path="basefunctions/threadpool/num_of_threads", default_value=10
    ),
    default_thread_pool_user_object=None,
)
