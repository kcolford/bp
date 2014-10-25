"""The version module for this package.

Whenever this module is imported, it will always attempt to update its
version string by fetching a new one from the VCS.  If that fails then
it retains the one that's already saved to it.

Currently, only git is a supported VCS.

"""

import re
import subprocess
import sys

def update():
    """Update this file with a new version string."""

    # Find ourself in sys.modules
    filename = sys.modules[__name__].__file__

    # Read our code into a string
    with open(filename) as f:
        code = f.read()

    # Substitute the default version string with whatever the current
    # one is.
    code = re.sub(r"^(\s*version = )'.*$", '\g<1>' + repr(version),
                  code, 1, re.M)

    # Write the new code back into the file.
    with open(filename, 'w') as f:
        f.write(code)

try:
    version = subprocess.check_output(['git', 'describe'])
    version = version.split()[0]
    update()
except OSError, CalledProcessError:
    version = 'v0.1'

