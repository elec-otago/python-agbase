import unittest
from getpass import getpass

__author__ = 'Tim Molteno'

class TestCommon(unittest.TestCase):
    testUser = "unittest@agbase.elec.ac.nz"
    testPwd = getpass('UnitTest Password: ')
    serverIp = "https://localhost:8443/api/"
