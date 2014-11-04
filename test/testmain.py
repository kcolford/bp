"""Test the main routine.

"""

import unittest
from txt2boil.main import main
import os

class TestDriver(unittest.TestCase):
    """Driver class that sets up the environment for the main file.

    """
    
    code = ''

    def setUp(self):
        with os.tmpfile() as f:
            
