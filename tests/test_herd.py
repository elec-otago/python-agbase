import unittest
from agbase.agbase import AgBase
import time
from test_common import TestCommon

__author__ = 'Tim Molteno'


class TestHerd(TestCommon):

    def setUp(self):
        self.agbase = AgBase()

        self.agbase.set_logging_on(True)

        self.user = self.agbase.connect(self.testUser, self.testPwd, self.serverIp)

        if self.user is None:
            self.fail()

        self.farm = self.agbase.create_farm("Python Test Farm")

    def tearDown(self):
        print('TestHerd.tearDown')
        self.agbase.remove_farm(self.farm)


    def test_get_nonexistent_herd(self):

        herds = self.agbase.get_herds(self.farm)

        if herds is not None and len(herds) != 0:
            self.fail()

        herd = self.agbase.create_herd(self.farm, "Python Test Herd")

        if herd is None:
            self.fail()

        herd2 = self.agbase.create_herd(self.farm, "Python Test Herd")

        if herd2 is None:
            self.fail()
            
        print herd2.id
            

    def test_herds(self):

        herd = self.agbase.create_herd(self.farm, "Python Test Herd")

        if herd is None:
            self.fail()

        print('created herd: {} with id: {}'.format(herd.name, herd.id))

        herds = self.agbase.get_herds()

        if herds is None:
            self.fail()

        for herd in herds:
            print('found herd: {} with id: {}'.format(herd.name, herd.id))

        herds = self.agbase.get_herds(self.farm)

        if herds is None:
            self.fail()

        for herd in herds:
            print('The farm "{}" has a herd named: {}'.format(self.farm.name, herd.name))

        deleted = self.agbase.remove_herd(herd)

        if not deleted:
            self.fail()



if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestHerd)
  unittest.TextTestRunner(verbosity=2).run(suite)
