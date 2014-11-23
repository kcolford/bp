"""This module contains a dynamic generator class.

It allows on the fly (at runtime) creation of generator classes for
things such as aliases and custom generators provided in spec files.

"""

from .core import *


class AliasGen(Gen, dict):

    """A generator that provides aliasing syntax."""

    def __missing__(self, key):
        return None
    
    def matchComment(self, comm):
        pass                    # TODO
