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


"""Update the boilerplate in source code.

We do so according to a series of marker comments found through
regexs.

"""

import argparse
import sys
from boil.langs import Racket


def update(text):
    """Update source code text to generate boilerplate.

    """

    return Racket().gen(text)


def readFrom(handle):
    """Read text from handle depending on what type it is.

    If it is a string then open it as a file.  Otherwise, treat it as
    a file-like object and call read on it.

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
    """Write text to handle depending on what type it is.

    If it is a string then open it as a file.  Otherwise, treat it as
    a file-like object and call write on it.

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
    """The main method."""

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

description = __doc__
epilog = ''

if __name__ == '__main__':
    main()
