 # Agbase - Measurement List
 # 
 # Copyright (c) 2015. Elec Research.
 # 
 # This Source Code Form is subject to the terms of the Mozilla Public
 # License, v. 2.0. If a copy of the MPL was not distributed with this
 # file, You can obtain one at http://mozilla.org/MPL/2.0/

__author__ = 'Tim Molteno, Mark Butler'

class MeasurementList:

    def __init__(self, animal, algorithm, user):
        self.animal = animal
        self.algorithm = algorithm
        self.user = user
        self.measurements = []


    def add_measurement(self, time_stamp, w05, w25=None, w50=None, w75=None, w95=None, comment=None):

        measurement_details = {'timeStamp': time_stamp, 'w05': w05}

        if w25 is not None:
            measurement_details['w25'] = w25

        if w50 is not None:
            measurement_details['w50'] = w50

        if w75 is not None:
            measurement_details['w75'] = w75

        if w95 is not None:
            measurement_details['w95'] = w95

        if comment is not None:
            measurement_details['comment'] = comment

        self.measurements.append(measurement_details)

    def get_measurement_count(self):
        return len(self.measurements)

    def get_json(self):

        if len(self.measurements) <= 0:
            return None

        json_list = {'farmId':self.animal.farm_id,
                     'animalId': self.animal.id,
                     'algorithmId': self.algorithm.id,
                     'userId': self.user.id,
                     'measurements': self.measurements}

        return json_list