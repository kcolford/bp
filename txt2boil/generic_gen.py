"""This module provides a universal generic generator.

The GenericGen encompasses all the generic generators available by
inheiriting from each and every one of them.  This makes it easy for
people to add languages because they can just have their class inherit
from this one so that their language will support all the available
features.

"""


# To add additional generators, just add an import statement that
# exposes the generator to the module level namespace.  The GenericGen
# class will pick it up automatically and generate the appropriate
# code for it.
from core import Gen
from linegen import LineCodeGen
from pygen import PyGen


# GenericGen will inherit from any class in module level scope that
# ends with the name Gen.
class GenericGen(*[cls for cls in globals().keys() if cls.endswith('Gen')]):

    """A generic generator.

    This includes the functionally of all language agnostic generators
    and as such can be used as the main parent class when defining a
    new language class.

    It also provides an easy way to add language agnostic generators
    to all the languages without editing each class file.  You simply
    add an import statement to the top of this module and GenericGen
    will take care of everything else.

    """

    pass


__all__ = ['GenericGen']
