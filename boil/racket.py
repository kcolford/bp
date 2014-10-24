from hookedre import HookedRegex
from extractor import Extractor
from linegen import LineCodeGen


class RacketComments(Extractor):
    """Extract Racket comments from source code.

    """

    __regex = re.compile(r'^;; (.*\n)', re.M)

    def lineComment(self, text, start):
        return self.__regex.search(text, start)


class RacketLineCodeGen(RacketComments, LineCodeGen):
    """Generate lines of code in Racket.

    """

    pass


class RacketConstantGen(RacketLineCodeGen):
    """Auto generate constants for Racket code.

    """
    
    def matchComment(self, comm):
        return (HookedRegex(r'Constant Gen: (\S+) (.*)\n',
                            '(define \g<0> {})\n',
                            comm) or
                super(RacketConstantGen, self).matchComment(comm))


class Racket(RacketConstantGen, RacketLineCodeGen):
    """Update all code found in a Racket sourcefile.

    """

    pass


__all__ = ['Racket']
