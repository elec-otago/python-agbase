 # Agbase - Unittest - Config
 # 
 # Copyright (c) 2015. Elec Research.
 # 
 # This Source Code Form is subject to the terms of the Mozilla Public
 # License, v. 2.0. If a copy of the MPL was not distributed with this
 # file, You can obtain one at http://mozilla.org/MPL/2.0/

import unittest
from getpass import getpass

__author__ = 'Tim Molteno'

class TestCommon(unittest.TestCase):
    testUser = "unittest@agbase.elec.ac.nz"
    testPwd = getpass('UnitTest Password: ')
    serverIp = "https://localhost:8443/api/"
