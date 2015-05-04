import unittest
from agbase.agbase import AgBase
import time
from test_common import TestCommon

__author__ = 'mark'


class TestAgBase(TestCommon):

    def setUp(self):
        print('TestAgBase.setUp')
        super(self.__class__, self).setUp()

        self.agbase = AgBase()

        self.agbase.set_logging_on(True)

        self.user = self.agbase.connect(self.testUser, self.testPwd, self.serverIp)

        if self.user is None:
            self.fail()

        print('connected to mooogle with user: {} with id: {}'.format(self.user.email, self.user.id))


    def test_farms(self):

        test_farm = self.agbase.create_farm("Python Test Farm")

        if test_farm is None:
            self.fail()

        print('created farm: {} with id: {}'.format(test_farm.name, test_farm.id))

        farms = self.agbase.get_farms()

        if farms is None:
            self.fail()

        for farm in farms:
            print('found farm: {} with id: {}'.format(farm.name, farm.id))

        single_query_farm = self.agbase.get_farm(test_farm.id)

        if single_query_farm.id != test_farm.id:
            self.fail()

        farms = self.agbase.get_farms(self.user)

        if farms is None:
            self.fail()

        for farm in farms:
            print('The current user can access farm: {}'.format(farm.name))

        deleted = self.agbase.remove_farm(test_farm)

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

        test_category = self.agbase.create_measurement_category('Test Category')

        if test_category is None:
            self.fail()

        print('created measurement category: {} with id: {}'.format(test_category.name, test_category.id))

        single_query_category = self.agbase.get_measurement_category(test_category.id)

        if test_category.id != single_query_category.id:
            self.fail()

        categories = self.agbase.get_measurement_categories()

        if categories is None:
            self.fail()

        for category in categories:
            print('found category: {}'.format(category.name))

        deleted = self.agbase.remove_measurement_category(test_category)

        if not deleted:
            self.fail()


    def test_algorithms(self):

        test_category = self.agbase.create_measurement_category('Algorithm Test Category')
        test_algorithm = self.agbase.create_algorithm('Test Algorithm', test_category)

        if test_algorithm is None:
            self.fail()

        print('created algorithm {} with id: {}'.format(test_algorithm.name, test_algorithm.id))

        single_query_algorithm = self.agbase.get_algorithm(test_algorithm.id)

        if test_algorithm.id != single_query_algorithm.id:
            self.fail()

        algorithms = self.agbase.get_algorithms()

        if algorithms is None:
            self.fail()

        for algorithm in algorithms:
            print('found algorithm: {}'.format(algorithm.name))

        deleted = self.agbase.remove_algorithm(test_algorithm)

        if not deleted:
            self.fail()

        self.agbase.remove_measurement_category(test_category)


    def test_animals(self):

        test_farm = self.agbase.create_farm('Animal Test Farm')
        test_herd = self.agbase.create_herd(test_farm, 'Animal Test Herd')

        test_eid = "AN-EID-FOR_TESTING"

        test_animal = self.agbase.create_animal(test_farm, test_eid)

        if test_animal is None:
            self.fail()

        print('created animal {} with id: {}'.format(test_animal.eid, test_animal.id))

        result = self.agbase.set_animal_herd(test_animal, test_herd)

        if result is None:
            self.fail()

        animals = self.agbase.get_animals(test_farm, test_herd)

        if animals is None:
            self.fail()

        for animal in animals:
            print('found animal: {}'.format(animal.eid))

        updated = self.agbase.update_animal_vid(test_animal, "My Pet Cow")

        if not updated:
            self.fail()

        expected_animal = self.agbase.get_animal_by_eid(test_farm, test_eid)

        if expected_animal.id != test_animal.id:
            self.fail()

        deleted = self.agbase.remove_animal(test_animal)

        if not deleted:
            self.fail()

        self.agbase.remove_herd(test_herd)
        self.agbase.remove_farm(test_farm)


    def test_measurements(self):

        test_farm = self.agbase.create_farm('Animal Test Farm')
        test_eid = "AN-EID-FOR_TESTING"
        test_animal = self.agbase.create_animal(test_farm, test_eid)
        test_category = self.agbase.create_measurement_category('Algorithm Test Category')
        test_algorithm = self.agbase.create_algorithm('Test Algorithm', test_category)

        measurement = self.agbase.create_measurement(test_animal, test_algorithm, self.user, time.strftime("%c"), 0.3344)

        if measurement is None:
            self.fail()

        print('created measurement with id {}'.format(measurement.id))

        animal_measurements = self.agbase.get_measurements_for_animal(test_animal)

        if animal_measurements[0].id != measurement.id:
            self.fail()

        deleted = self.agbase.remove_measurement(measurement)

        if not deleted:
            self.fail()

        eid_measurement = self.agbase.create_measurement_for_eid(test_eid, test_farm, test_algorithm, self.user, time.strftime("%c"), 0.3344)

        if eid_measurement is None:
            self.fail()

        if eid_measurement.animal_id != test_animal.id:
            self.fail()

        self.agbase.remove_measurement(eid_measurement)

        self.agbase.remove_animal(test_animal)
        self.agbase.remove_farm(test_farm)
        self.agbase.remove_algorithm(test_algorithm)
        self.agbase.remove_measurement_category(test_category)


    def test_measurements_bulk_upload(self):

        test_farm = self.agbase.create_farm('Animal Test Farm')
        test_eid = "AN-EID-FOR_TESTING"
        test_animal = self.agbase.create_animal(test_farm, test_eid)
        test_category = self.agbase.create_measurement_category('Algorithm Test Category')
        test_algorithm = self.agbase.create_algorithm('Test Algorithm', test_category)

        measurement_list = self.agbase.create_bulk_measurement_upload_list(test_animal, test_algorithm, self.user)

        measurement_list.add_measurement(time.strftime("%c"), 0.3344)
        measurement_list.add_measurement(time.strftime("%c"), 0.4455)
        measurement_list.add_measurement(time.strftime("%c"), 0.5566)

        success = self.agbase.upload_measurement_list(measurement_list)

        if success is not True:
            self.fail()

        print('created bulk measurements')

        animal_measurements = self.agbase.get_measurements_for_animal(test_animal)

        if len(animal_measurements) != 3:
            self.fail()

        self.agbase.remove_animal(test_animal)
        self.agbase.remove_farm(test_farm)
        self.agbase.remove_algorithm(test_algorithm)
        self.agbase.remove_measurement_category(test_category)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestAgBase)
  unittest.TextTestRunner(verbosity=2).run(suite)
