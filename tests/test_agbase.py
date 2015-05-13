 # Agbase - Unittest - Tests
 # 
 # Copyright (c) 2015. Elec Research.
 # 
 # This Source Code Form is subject to the terms of the Mozilla Public
 # License, v. 2.0. If a copy of the MPL was not distributed with this
 # file, You can obtain one at http://mozilla.org/MPL/2.0/

import unittest
from agbase.agbase import AgBase
from agbase.algorithm import AlgorithmAPI
from agbase.animal import AnimalAPI
from agbase.farm import FarmAPI
from agbase.herd import HerdAPI
from agbase.measurement import MeasurementAPI
from agbase.measurement_category import MeasurementCategoryAPI
import pprint
import time
from test_common import TestCommon

__author__ = 'mark'


class TestAgBase(TestCommon):

    def setUp(self):
        print('TestAgBase.setUp')
        super(self.__class__, self).setUp()
        self.pp = pprint.PrettyPrinter(indent=4)
        self.agbase = AgBase()
        self.algorithm = AlgorithmAPI(self.agbase)
        self.animal = AnimalAPI(self.agbase)
        self.farm = FarmAPI(self.agbase)
        self.herd = HerdAPI(self.agbase)
        self.measurement = MeasurementAPI(self.agbase)
        self.measurement_category = MeasurementCategoryAPI(self.agbase)

        self.agbase.set_logging_on(True)

        self.user = self.agbase.connect(self.testUser, self.testPwd, self.serverIp)

        if self.user is None:
            self.fail()

        print('connected to mooogle with user: {} with id: {}'.format(self.user.email, self.user.id))


    def test_farms(self):

        test_farm = self.farm.create_farm("Python Test Farm")

        if test_farm is None:
            self.fail()

        print('created farm: {} with id: {}'.format(test_farm.name, test_farm.id))

        farms = self.farm.get_farms()

        if farms is None:
            self.fail()

        for farm in farms:
            print('found farm: {} with id: {}'.format(farm.name, farm.id))

        single_query_farm = self.farm.get_farm(test_farm.id)

        if single_query_farm.id != test_farm.id:
            self.fail()

        farms = self.farm.get_farms(self.user)

        if farms is None:
            self.fail()

        for farm in farms:
            print('The current user can access farm: {}'.format(farm.name))

        deleted = self.farm.remove_farm(test_farm)

        if not deleted:
            self.fail()


    def test_roles(self):

        roles = self.agbase.get_roles()

        if roles is None:
            self.fail()

        for role in roles:
            print('Found role named {}'.format(role.name))


    def test_users(self):

        roles = self.agbase.get_roles()

        admin_role = None

        for role in roles:
            if role.name == "Viewer":
                admin_role = role
                break

        test_user = self.agbase.create_user("Test", "Testor", "test@test.com", "testpass", admin_role)

        if test_user is None:
            self.fail()

        print('created user: {} with id: {}'.format(test_user.email, test_user.id))

        users = self.agbase.get_users()

        if users is None:
            self.fail()

        for user in users:
            print('found user: {} {} with email: {}'.format(user.first_name, user.last_name, user.email))

        deleted = self.agbase.remove_user(test_user)

        if not deleted:
            self.fail()


    def test_measurement_categories(self):

        test_category = self.measurement_category.create_measurement_category('Test Category')

        if test_category is None:
            self.fail()

        print('created measurement category: {} with id: {}'.format(test_category.name, test_category.id))

        single_query_category = self.measurement_category.get_measurement_category(test_category.id)

        if test_category.id != single_query_category.id:
            self.fail()

        categories = self.measurement_category.get_measurement_categories()

        if categories is None:
            self.fail()

        for category in categories:
            print('found category: {}'.format(category.name))

        deleted = self.measurement_category.remove_measurement_category(test_category)

        if not deleted:
            self.fail()


    def test_algorithms(self):

        test_category = self.measurement_category.create_measurement_category('Algorithm Test Category')
        test_algorithm = self.algorithm.create_algorithm('Test Algorithm', test_category)

        if test_algorithm is None:
            self.fail()

        print('created algorithm {} with id: {}'.format(test_algorithm.name, test_algorithm.id))

        single_query_algorithm = self.algorithm.get_algorithm(test_algorithm.id)

        if test_algorithm.id != single_query_algorithm.id:
            self.fail()

        algorithms = self.algorithm.get_algorithms()

        if algorithms is None:
            self.fail()

        for algorithm in algorithms:
            print('found algorithm: {}'.format(algorithm.name))

        deleted = self.algorithm.remove_algorithm(test_algorithm)

        if not deleted:
            self.fail()

        self.measurement_category.remove_measurement_category(test_category)


    def test_animals(self):

        test_farm = self.farm.create_farm('Animal Test Farm')
        test_herd = self.herd.create_herd(test_farm, 'Animal Test Herd')

        test_eid = "AN-EID-FOR_TESTING"

        test_animal = self.animal.create_animal(test_farm, test_eid)

        if test_animal is None:
            self.fail()

        print('created animal {} with id: {}'.format(test_animal.eid, test_animal.id))

        result = self.animal.set_animal_herd(test_animal, test_herd)

        if result is None:
            self.fail()

        animals = self.animal.get_animals(test_farm, test_herd)

        if animals is None:
            self.fail()

        for animal in animals:
            print('found animal: {}'.format(animal.eid))

        updated = self.animal.update_animal_vid(test_animal, "My Pet Cow")

        if not updated:
            self.fail()

        expected_animal = self.animal.get_animal_by_eid(test_farm, test_eid)

        if expected_animal.id != test_animal.id:
            self.fail()

        deleted = self.animal.remove_animal(test_animal)

        if not deleted:
            self.fail()

        self.herd.remove_herd(test_herd)
        self.farm.remove_farm(test_farm)


    def test_measurements(self):

        test_farm = self.farm.create_farm('Animal Test Farm')
        test_eid = "AN-EID-FOR_TESTING"
        test_animal = self.animal.create_animal(test_farm, test_eid)
        test_category = self.measurement_category.create_measurement_category('Algorithm Test Category')
        test_algorithm = self.algorithm.create_algorithm('Test Algorithm', test_category)

        measurement = self.measurement.create_measurement(test_animal, test_algorithm, self.user, time.strftime("%c"), None, None, 0.3344,None,None,None)

        if measurement is None:
            self.fail()

        print('created measurement with id {}'.format(measurement.id))

        animal_measurements = self.measurement.get_measurements_for_animal(test_animal)

        if animal_measurements[0].id != measurement.id:
            self.fail()

        deleted = self.measurement.remove_measurement(measurement)

        if not deleted:
            self.fail()

        eid_measurement = self.measurement.create_measurement_for_eid(test_animal.eid,test_farm, test_algorithm, self.user, time.strftime("%c"), None, None, 0.3344,None,None,None)

        if eid_measurement is None:
            self.fail()

        if eid_measurement.animal_id != test_animal.id:
            self.fail()
        #self.pp.pprint(repr(eid_measurement))
        for keys,values in eid_measurement.__repr__().items():
            print(keys)
            print(values)
        self.measurement.remove_measurement(eid_measurement)

        self.animal.remove_animal(test_animal)
        self.farm.remove_farm(test_farm)
        self.algorithm.remove_algorithm(test_algorithm)
        self.measurement_category.remove_measurement_category(test_category)


    def test_measurements_bulk_upload(self):

        test_farm = self.farm.create_farm('Animal Test Farm')
        test_eid = "AN-EID-FOR_TESTING"
        test_animal = self.animal.create_animal(test_farm, test_eid)
        test_category = self.measurement_category.create_measurement_category('Algorithm Test Category')
        test_algorithm = self.algorithm.create_algorithm('Test Algorithm', test_category)

        measurement_list = self.measurement.create_bulk_measurement_upload_list(test_animal, test_algorithm, self.user)

        measurement_list.add_measurement(time.strftime("%c"), 0.3344)
        measurement_list.add_measurement(time.strftime("%c"), 0.4455)
        measurement_list.add_measurement(time.strftime("%c"), 0.5566)

        success = self.measurement.upload_measurement_list(measurement_list)

        if success is not True:
            self.fail()

        print('created bulk measurements')

        animal_measurements = self.measurement.get_measurements_for_animal(test_animal)

        if len(animal_measurements) != 3:
            self.fail()

        self.animal.remove_animal(test_animal)
        self.farm.remove_farm(test_farm)
        self.algorithm.remove_algorithm(test_algorithm)
        self.measurement_category.remove_measurement_category(test_category)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestAgBase)
  unittest.TextTestRunner(verbosity=2).run(suite)
