"""Cooprative Multiple Inheritance made easy.

This module provides a function descriptor that transforms an ordinary
overloaded function into a function that behaves with the style of
Cooperative Multiple Inheritance (CMI) so as to mimic the Chain of
Resposibility design pattern.

There are two API's: one is the generic descripter that takes a binary
operation and uses it to merge two answers together.  The other is two
functions: one which locates the first non-None object and returns it,
and the other which finds the minimum element of all the posibilities.

"""

from functools import wraps

class AbstractCMI:

    """A descriptor that enables easy CMI according to a function.

    The final result function will be achieved by using merge as a
    binary operation on the results of the current function and the
    super-class' function of the same name.

    """

    def __init__(self, cls, merge):
        """Initialize the abstract descriptor.
        
        cls   - the current class
        merge - the binary operator that will determine the final
                result

        """

        self.cls = cls
        self.merge = merge

    def __call__(self, func):
        """Apply this abstract descriptor to func."""

        @wraps(func)
        def wrapper(s, *args, **kwargs):
            a = func(s, *args, **kwargs)
            b = getattr(super(self.cls, s), func.__name__)(*args, **kwargs)
            return self.merge(a, b)
        return wrapper


def minCMI(cls):
    """Return an AbstractCMI that locates the minimum element."""

    return AbstractCMI(cls, min)

def notNoneCMI(cls):
    """Return an AbstractCMI that locates the first non-None element."""

    return AbstractCMI(cls, lambda x, y: x if x is not None else y)

__all__ = ['AbstractCMI', 'minCMI', 'notNoneCMI']
