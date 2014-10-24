from boil.core import Extractor
import re


class Shell(Extractor):

    """Handle Python comments.

    """

    __regex = re.compile(r'^# (.*\n)', re.M)

    def lineComment(self, text, start):
        return self.__regex.search(text, start)


class Lisp(Extractor):

    """Extract Racket comments from source code.

    """

    __regex = re.compile(r'^;; (.*\n)', re.M)

    def lineComment(self, text, start):
        return self.__regex.search(text, start)
