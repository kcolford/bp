from core.gen import Gen
from linegen import LineCodeGen
import comments

class Python(comments.Shell, LineCodeGen):

    """Update all code found in a Python source file.

    """

    pass

class RacketConstantGen(Gen):

    """Auto generate constants for Racket code.

    """

    def matchComment(self, comm):
        return (HookedRegex(r'Constant Gen: (\S+) (.*)\n',
                            '(define \g<0> {})\n',
                            comm) or
                super(RacketConstantGen, self).matchComment(comm))


class Racket(RacketConstantGen, comments.Lisp, LineCodeGen):

    """Update all code found in a Racket sourcefile.

    """

    pass


__all__ = ['Python', 'Racket']
