#!/usr/bin/python

# Copyright (C) 2014 Kieran Colford

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
# <http://www.gnu.org/licenses/>.


"""A boilerplate generator.

"""

import argparse
import itertools
import re
import sys

try:
    from blist import blist
except ImportError:
    blist = list


class HookedRegex(object):
    """A regex object with a hook that generates output from what it has
    matched.

    """

    def __new__(cls, match, template, text):
        if re.match(match, text, re.M) is None:
            return None
        return super(HookedRegex, cls).__new__(cls, match, template, text)

    def __init__(self, match, template, text):
        """Initialize the object as a clone of another regex, but add a hook
        to it this time.

        """

        self.regex = re.match(match, text, re.M)
        self.template = template

    def __bool__(self):
        return self.regex is not None
        
    def group(self, n=0):
        return self.regex.group(n)

    def output(self, match):
        return match.expand(self.template.format(self.regex.group(2)))


class Extractor(object):
    """A class that extracts the comments from source code text.

    """

    _emptylineregex = re.compile('^()$^$', re.M)
    
    def lineComment(self, text, start):
        """Return a match object for a line comment in text starting at start.

        Overload this method to control what comments are matched.

        """

        pass

    def blockComment(self, text, start):
        """Return a match object for a block comment in text starting at
        start.

        Overload this method to control how block comments are
        matched.

        """

        pass

    def nextComment(self, text, start=0):
        """Return the next comment found in text starting at start.

        """

        m = min([self.lineComment(text, start),
                 self.blockComment(text, start),
                 self._emptylineregex.search(text, start)],
                key=lambda m: m.start(0) if m else len(text))
        return m

    def hasLineComment(self, text):
        """Return true if text contains a line comment.

        """
        
        return self.lineComment(text, 0) is not None 

    def isLineComment(self, text):
        """Return true if the text is a line comment.

        """
        
        m = self.lineComment(text, 0)
        return m and m.start(0) == 0 and m.end(0) == len(text)

    def nextValidComment(self, text, start=0):
        """Return the next actual comment.

        """
        
        m = min([self.lineComment(text, start),
                 self.blockComment(text, start)],
                key=lambda m: m.start(0) if m else len(text))
        return m


    def extractContent(self, text):
        """Extract the content of comment text.

        """

        m = self.nextValidComment(text)
        return '' if m is None else m.group(1)

    def extractChunkContent(self, lst):
        """Extract the content of a chunk (a list of comments) and represent
        that as a single string.

        """

        return ''.join(map(self.extractContent, lst))

    def chunkComment(self, text, start=0):
        """Return a list of chunks of comments.

        """

        # Build a list of comments
        comm, out = self.nextComment(text, start), []
        while comm:
            out.append(comm.group(0))
            comm = self.nextComment(text, comm.start(0) + 1)
        
        # Collect the comments according to whether they are line
        # comments or block comments.
        out = [list(g) for (_, g) in 
               itertools.groupby(out, self.isLineComment)]

        out = [i for i in out if i != ['']]
        
        return out
    
    def comments(self, text, start=0):
        """Return a list of comments.

        """

        out = [self.extractChunkContent(s) 
               for s in self.chunkComment(text, start)]
        return out

    def code(self, text):
        """Return the code instead of the comments.

        """

        comm = self.nextValidComment(text)
        while comm:
            text = text[:comm.start()] + text[comm.end():]
            comm = self.nextValidComment(text, comm.end(0))
        return text


class Gen(Extractor):
    """The generator class for boilerplate code.

    """

    def matchComment(self, comm):
        """Return a HookedRegex according to what comments this generator
        looks at.

        Overload this method to match different comments.

        """
        
        pass

    def collectTriggers(self, rgx, code):
        """Return a dictionary of triggers and their corresponding matches
        from the code.

        """

        return { m.group(0):m for m in re.finditer(rgx, code) }

    def genOutputs(self, code, match):
        """Return a list out template outputs based on the triggers found in
        the code and the template they create.

        """
        
        out = sorted((k, match.output(m)) for (k, m) in 
                     self.collectTriggers(match.group(1), code).items())
        out = list(map(lambda a: a[1], out))
        return out

    def gen(self, text, start=0):
        """Return the source code in text, filled with autogenerated code
        starting at start.

        """

        assert type(self) is not Gen
        # if type(self) is Gen:
        #     return text
        
        for cc in self.chunkComment(text, start):
            c = self.extractChunkContent(cc)
            cc = ''.join(cc)
            m = self.matchComment(c)
            idx = text.index(cc, start)
            e = idx + len(cc)
            if m:
                assert text[idx:e] == cc
                
                try:
                    end = text.index('\n\n', e - 1) + 1
                except ValueError:
                    end = len(text)
                text = text[:e] + text[end:]
                new = self.genOutputs(self.code(text), m)
                new = ''.join(new)
                text = text[:e] + new + text[e:]

                return self.gen(text, e + len(new))
        return text


class LineCodeGen(Gen):
    """Generate code on a line by line basis.
    
    """

    def matchComment(self, comm):
        return (HookedRegex(r'Line Gen:\n(.+)\n(.+)\n',
                            '{}\n',
                            comm) or
                super(LineCodeGen, self).matchComment(comm))
        

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


def update(text):
    """Update source code text to generate boilerplate.

    """

    return Racket().gen(text)

def readFrom(handle):
    """Read text from handle depending on what type it is.  If it is a
    string then open it as a file.  Otherwise, treat it as a file-like
    object and call read on it.

    """

    if isinstance(handle, str):
        if handle == '-':
            return sys.stdin.read()
        else:
            with open(handle, 'r') as f:
                return f.read()
    else:
        return handle.read()

def writeInto(handle, text):
    """Write text to handle depending on what type it is.  If it is a
    string then open it as a file.  Otherwise, treat it as a file-like
    object and call write on it.

    """

    if isinstance(handle, str):
        if handle == '-':
            sys.stdout.write(text)
        else: 
            with open(handle, 'w') as f:
                f.write(text)
    else:
        handle.write(text)

def updateStream(fin, fout):
    """Update a stream from fin and put the output in fout.

    """

    text = readFrom(fin)
    text = update(text)
    writeInto(fout, text)

def updateFile(fname):
    """Update a file in place.

    """

    updateStream(fname, fname)    

def main():
    """Update the boilerplate in source code according to a series of
    marker comments.

    """

    parser = argparse.ArgumentParser(description=description,
                                     epilog=epilog)
    parser.add_argument('-i', '--inplace', help='modify files inplace',
                        action='store_true')
    parser.add_argument('-f', '--files', help='the files to update',
                        action='append')
    parser.add_argument('-t', '--tests', '--run-tests',
                        help='run the testsuites',
                        action='store_true')
    args = parser.parse_args()
    if args.tests:
        unittest.main()
    elif args.files:
        for f in args.files:
            if args.inplace:
                updateFile(f)
            else:
                updateStream(f, sys.stdout)
    else:
        parser.print_help()

description = __doc__ + main.__doc__
epilog = ''

if __name__ == '__main__':
    main()

