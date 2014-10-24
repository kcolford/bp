from extractor import Extractor
from linegen import LineCodeGen


class PythonComments(Extractor):
    """Handle Python comments.

    """

    __regex = re.compile(r'^# (.*\n)', re.M)

    def lineComment(self, text, start):
        return self.__regex.search(text, start)


class Python(PythonComments, LineCodeGen):
    """Update all code found in a Python source file.

    """

    pass


__all__ = ['Python']
