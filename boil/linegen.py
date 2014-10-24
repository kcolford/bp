from gen import Gen
from hookedre import HookedRegex


class LineCodeGen(Gen):

    """Generate code on a line by line basis.

    """

    def matchComment(self, comm):
        return (HookedRegex(r'Line Gen:\n(.+)\n(.+)\n',
                            '{}\n',
                            comm) or
                super(LineCodeGen, self).matchComment(comm))
