import unittest

def suite():
    return unittest.TestLoader().discover("website.tests", pattern="*.py")