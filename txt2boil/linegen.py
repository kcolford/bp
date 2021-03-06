# Copyright (C) 2014 Kieran Colford
#
# This file is part of txt2boil.
#
# txt2boil is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# txt2boil is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with txt2boil.  If not, see <http://www.gnu.org/licenses/>.

from .core import *
from . import cmi


class LineCodeGen(Gen):

    """Generate code on a line by line basis.

    """

    @cmi.nonNoneCMI(lambda: LineCodeGen)
    def matchComment(self, comm):
        return HookedRegex(r'Line Gen:\n(.+)\n(.+)\n',
                           '{}\n', comm)
