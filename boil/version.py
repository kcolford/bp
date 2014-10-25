"""The version module for this package.

Whenever this module is imported, it will always attempt to update its
version string by fetching a new one from the VCS.  If that fails then
it retains the one that's already saved to it.

Currently, only git is a supported VCS.

"""

import os
import re
import subprocess
import sys

def getDir():
    """Return the directory that this file is in."""

    thisfile = sys.modules[__name__].__file__
    thisdir = os.path.dirname(thisfile)

    return thisdir

def makeIgnorefile():
    """Verify the VCS ignore file is in place.

    This is meant to hide generated _version.py file.

    """

    ignorepath = os.path.join(getDir(), '.gitignore')
    if os.path.exists(ignorepath):
        with open(ignorepath, 'a') as f:
            f.write('/_version.py\n')
    else:
        with open(ignorepath, 'w') as f:
            f.write('/_version.py\n' + '/.gitignore\n')

def updateCache(ver):
    """Update the cache file with the version string ver."""

    with open(os.path.join(getDir(), '_version.py'), 'w') as f:
        f.write('version = ' + repr(ver))

def getVersion():
    """Return the version string.

    We'll update the _version.py file found in the package if we can.
    This is where the version string is cached incase the package is
    distributed outside of of a git repository.

    """

    try:
        import _version
    except ImportError:
        # There's no auto generated _version.py file, so we have to
        # make one.
        makeIgnorefile()        # Write the .gitignore
        updateCache('error')    # Initialize the cache file
        import _version         # Load the cache module
    
    try:
        ver = subprocess.check_output(
            ['git', 'describe','--abbrev=3', '--always'])
        ver = ver.strip('\n')
        updateCache(ver)
    except OSError, CalledProcessError:
        ver = _version.version

    return ver

version = getVersion()
__all__ = ['version']
