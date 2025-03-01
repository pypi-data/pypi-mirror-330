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
#  a simple observer pattern
#
# =============================================================================
"""

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------

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
class Observer:
    """
    The Observer interface declares the update method, used by subjects.
    """

    def update(self, message: any, *args, **kwargs) -> None:
        """
        Receive update from subject.

        Parameters:
        -----------
        message : any
            The message sent by the subject to the Observers.
        """


class Subject:
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the list of subscribers.
        """
        self._observers = []

    def attach_observer(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.

        Parameters:
        -----------
        observer : Observer
            The observer to attach to the subject.
        """
        self._observers.append(observer)

    def detach_observer(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.

        Parameters:
        -----------
        observer : Observer
            The observer to detach from the subject.
        """
        self._observers.remove(observer)

    def notify_observers(self, message: any, *args, **kwargs) -> None:
        """
        Notify all observers about an event.

        Parameters:
        -----------
        message : any
            The message to send to the observers.
        args: any
            Additional arguments to pass to the observers.
        kwargs: any
            Additional keyword arguments to pass to the observers.
        """
        for observer in self._observers:
            observer.update(message, *args, **kwargs)
