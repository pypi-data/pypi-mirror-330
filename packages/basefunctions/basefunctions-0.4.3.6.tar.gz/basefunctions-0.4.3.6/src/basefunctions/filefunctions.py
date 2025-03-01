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
#  filefunctions provide basic functionality for file handling stuff
#
# =============================================================================
"""

import fnmatch

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
import os
import shutil
from typing import List

# -------------------------------------------------------------
# DEFINITIONS
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


def check_if_file_exists(file_name: str) -> bool:
    """
    Check if a file exists.

    Parameters
    ----------
    file_name : str
        The name of the file to be checked.

    Returns
    -------
    bool
        True if the file exists, False otherwise.
    """
    if file_name:
        return check_if_exists(file_name, file_type="FILE")
    return False


def check_if_dir_exists(dir_name: str) -> bool:
    """
    Check if directory exists.

    Parameters
    ----------
    dir_name : str
        Directory name to be checked.

    Returns
    -------
    bool
        True if directory exists, False otherwise.
    """
    if dir_name:
        return check_if_exists(dir_name, file_type="DIRECTORY")
    return False


def check_if_exists(file_name: str, file_type: str = "FILE") -> bool:
    """
    Check if a specific file or directory exists.

    Parameters
    ----------
    file_name : str
        Name of the file or directory to be checked.
    file_type : str, optional
        Type of file or directory to be checked, by default "FILE".

    Returns
    -------
    bool
        True if the file or directory exists, False otherwise.
    """
    if file_type == "FILE":
        return os.path.exists(file_name) and os.path.isfile(file_name)
    if file_type == "DIRECTORY":
        return os.path.exists(file_name) and os.path.isdir(file_name)
    return False


def is_file(file_name: str) -> bool:
    """
    Check if file_name is a regular file.

    Parameters
    ----------
    file_name : str
        Name of the file to be checked.

    Returns
    -------
    bool
        True if the file exists and is a regular file.
    """
    return check_if_file_exists(file_name)


def is_directory(dir_name: str) -> bool:
    """
    Check if `dir_name` is a regular directory.

    Parameters
    ----------
    dir_name : str
        Name of the directory to be checked.

    Returns
    -------
    bool
        True if the directory exists and is a directory, False otherwise.
    """
    return check_if_dir_exists(dir_name)


def get_file_name(path_file_name: str) -> str:
    """
    Get the file name part from a complete file path.

    Parameters
    ----------
    path_file_name : str
        The complete file path.

    Returns
    -------
    str
        The file name part of the file path.

    Examples
    --------
    > get_file_name('/home/usr/Desktop/2352222.pdf')
    '2352222.pdf'
    """
    return os.path.basename(path_file_name) if path_file_name or path_file_name == "" else ""


def get_file_extension(path_file_name: str) -> str:
    """
    Get the file extension from a complete file name.

    Parameters
    ----------
    pathFileName : str
        The path file name to get the file extension from.

    Returns
    -------
    str
        The file extension of the file name.

    Examples
    --------
    > getFileExtension('/home/usr/Desktop/2352222.abc.pdf')
    '.pdf'
    """
    extension = os.path.splitext(path_file_name)[-1] if path_file_name else ""
    if extension in [None, "."]:
        return ""
    return extension


def get_path_name(path_file_name: str) -> str:
    """
    Get the path name from a complete file name.

    Parameters
    ----------
    path_file_name : str
        The path file name to get information from.

    Returns
    -------
    str
        The path name of the file name.
    """
    return (
        os.path.normpath(os.path.split(path_file_name)[0]) + os.path.sep
        if path_file_name or path_file_name == ""
        else ""
    )


def get_parent_path_name(path_file_name: str) -> str:
    """
    Get the parent path name from a complete file name.

    Parameters
    ----------
    path_file_name : str
        The path file name to get information from.

    Returns
    -------
    str
        The parent path name.

    Examples
    --------
    > get_parent_path_name('/home/usr/Desktop/file.txt')
    '/home/usr/'
    """
    return (
        os.path.normpath(os.path.split(os.path.split(path_file_name)[0])[0]) + os.path.sep
        if path_file_name
        else ""
    )


def get_home_path() -> str:
    """
    Get the home path of the user.

    Returns
    -------
    str
        The home path of the user.

    Examples
    --------
    > get_home_path()
    '/home/usr/neutro2/'
    """
    return os.path.expanduser("~")


def get_base_name(path_file_name: str) -> str:
    """
    Get the base name part from a complete file name.

    Parameters
    ----------
    path_file_name : str
        The path file name to get information from.

    Returns
    -------
    str
        The base name of the file.

    Examples
    --------
    > get_base_name('/home/usr/Desktop/file.txt')
    /'file.txt'
    """
    return get_file_name(path_file_name)


def get_base_name_prefix(path_file_name: str) -> str:
    """
    Get the basename prefix from a complete file name.

    Parameters
    ----------
    path_file_name : str
        The path file name to get information from.

    Returns
    -------
    str
        The basename prefix of the file name.

    Examples
    --------
    > get_base_name_prefix('/home/usr/Desktop/file.abc.txt')
    'file.abc'
    """
    return (
        get_base_name(path_file_name).split(".")[0]
        if path_file_name or path_file_name == ""
        else ""
    )


def get_extension(path_file_name: str) -> str:
    """
    Get the extension from a complete file name.

    Parameters
    ----------
    path_file_name : str
        The path file name to get the extension from.

    Returns
    -------
    str
        The extension of the file name.

    Examples
    --------
    > get_extension('/home/usr/Desktop/2352222.pdf')
    '.pdf'
    """
    return (
        get_base_name(path_file_name).split(".")[-1]
        if path_file_name or path_file_name == ""
        else ""
    )


def get_path_and_base_name_prefix(path_file_name: str) -> str:
    """
    Get the path and base name from a complete file name.

    Parameters
    ----------
    path_file_name : str
        The path file name to get information from.

    Returns
    -------
    str
        The path and base name of the file name.
    """
    return (
        os.path.normpath(os.path.splitext(path_file_name)[0])
        if path_file_name or path_file_name == ""
        else ""
    )


def get_current_directory() -> str:
    """
    Get the current directory of the process.

    Returns
    -------
    str
        The name of the current directory.
    """
    return os.getcwd()


def set_current_directory(directory_name: str) -> None:
    """
    Set the current directory of the process.

    Parameters
    ----------
    directory_name : str
        The name of the directory to set as the current directory.

    Raises
    ------
    RuntimeError
        If the specified directory does not exist.

    """
    if directory_name not in [".", ".."] and not check_if_dir_exists(directory_name):
        raise RuntimeError(f"Directory '{directory_name}' not found.")
    os.chdir(directory_name)


def rename_file(src: str, target: str, overwrite=False) -> None:
    """Rename a file.

    This function renames a file from the source path to the target path.
    It can also handle cases where the target file already exists and
    provides an option to overwrite it.

    Parameters
    ----------
    src : str
        The source file name or path.
    target : str
        The target file name or path.
    overwrite : bool, optional
        Flag indicating whether to overwrite the target file if it already
        exists. If set to False and the target file exists, a RuntimeError
        will be raised. Default is False.

    Raises
    ------
    FileNotFoundError
        If the target directory doesn't exist.
    FileExistsError
        If the target file already exists and overwrite flag is set to False.
    FileNotFoundError
        If the source file doesn't exist.
    """
    # check if target directory exists if available
    dir_name = get_path_name(target)
    if not dir_name or not check_if_dir_exists(dir_name):
        raise FileNotFoundError(f"{dir_name} doesn't exist, can't rename file")
    # check if target file exists already and we should not overwrite it
    if overwrite is False and check_if_file_exists(target):
        raise FileExistsError(f"{target} already exists and overwrite flag set False")
    # check if source file exists
    if check_if_file_exists(src):
        os.rename(src, target)
    else:
        raise FileNotFoundError(f"{src} doesn't exist")


def remove_file(file_name: str) -> None:
    """Remove a file.

    This function removes the specified file if it exists.

    Parameters
    ----------
    file_name : str
        The name of the file to remove.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.

    """
    if check_if_file_exists(file_name):
        os.remove(file_name)


def create_directory(dir_name: str) -> None:
    """Create a directory recursively.

    This function creates a directory recursively, which means a complete path
    to the requested structure will be created if it doesn't exist yet.

    Parameters
    ----------
    dir_name : str
        Directory path to create.

    Returns
    -------
    None
        This function does not return anything.

    Raises
    ------
    OSError
        If there is an error while creating the directory.

    """
    os.makedirs(dir_name, exist_ok=True)


def remove_directory(dir_name: str) -> None:
    """Remove a directory.

    This function removes the specified directory and all its contents
    recursively.

    Parameters
    ----------
    dir_name : str
        The name of the directory to be removed.

    Raises
    ------
    RuntimeError
        Raises a RuntimeError when trying to remove the root directory ('/').

    """
    if not check_if_dir_exists(dir_name):
        return
    if dir_name == os.path.sep or dir_name == "/":
        raise RuntimeError("Can't delete the root directory ('/')")
    shutil.rmtree(dir_name)


def create_file_list(
    pattern_list: List[str] | None = None,
    dir_name: str = "",
    recursive: bool = False,
    append_dirs: bool = False,
    add_hidden_files: bool = False,
    reverse_sort: bool = False,
) -> List[str]:
    """
    Create a file list from a given directory.

    Parameters
    ----------
    pattern_list : list[str], optional
        Pattern elements to search for. If None, all files and directories are
        included. Default is ["*"].
    dir_name : str, optional
        Directory to search. If None, the current directory is used.
        Default is None.
    recursive : bool, optional
        Recursive search. Default is False.
    append_dirs : bool, optional
        Append directories matching the patterns. Default is False.
    add_hidden_files : bool, optional
        Append hidden files matching the patterns. Default is False.
    reverse_sort : bool, optional
        Reverse sort the result list. Default is False.

    Returns
    -------
    list
        List of files and directories matching the patterns.
    """
    if pattern_list is None:
        pattern_list = ["*"]
    result_list: List[str] = []
    if not dir_name:
        dir_name = "."
    if not (dir_name.startswith(os.path.sep) or ":" in dir_name) and not dir_name.startswith("."):
        dir_name = f".{os.path.sep}{dir_name}"
    if not isinstance(pattern_list, list):
        pattern_list = [pattern_list]
    if not check_if_dir_exists(dir_name):
        return result_list
    for file_name in os.listdir(dir_name):
        for pattern in pattern_list:
            if recursive and os.path.isdir(os.path.sep.join([dir_name, file_name])):
                result_list.extend(
                    create_file_list(
                        pattern_list,
                        os.path.sep.join([dir_name, file_name]),
                        recursive,
                        append_dirs,
                        add_hidden_files,
                        reverse_sort,
                    )
                )
            if fnmatch.fnmatch(file_name, pattern):
                if append_dirs and os.path.isdir(os.path.sep.join([dir_name, file_name])):
                    result_list.append(file_name)
                if is_file(os.path.sep.join([dir_name, file_name])):
                    if not add_hidden_files and file_name.startswith("."):
                        continue
                    result_list.append(os.path.sep.join([dir_name, file_name]))
    result_list.sort(reverse=reverse_sort)
    return result_list


def norm_path(file_name: str) -> str:
    """
    Normalize a path.

    Parameters
    ----------
    file_name : str
        File name to normalize.

    Returns
    -------
    str
        Normalized path name.
    """
    return os.path.normpath(file_name.replace("\\", "/"))
