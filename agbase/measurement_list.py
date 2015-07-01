 # Agbase - Measurement List
 # 
 # Copyright (c) 2015. Elec Research.
 # 
 # This Source Code Form is subject to the terms of the Mozilla Public
 # License, v. 2.0. If a copy of the MPL was not distributed with this
 # file, You can obtain one at http://mozilla.org/MPL/2.0/

__author__ = 'Tim Molteno, Mark Butler'

class MeasurementList:

    def __init__(self, algorithm, user,animal=None,farmId=None):
        if(animal is not None):
            self.animal = animal
        else:
            self.animal = None
            self.farm_id = farmId

        self.algorithm = algorithm
        self.user = user
        self.measurements = []


    def add_measurement(self, time_stamp, w05, w25, w50, w75, w95, eid=None):

        measurement_details = {'timeStamp': time_stamp, 'w05': w05}

        if w25 is not None:
            measurement_details['w25'] = w25

        if w50 is not None:
            measurement_details['w50'] = w50

        if w75 is not None:
            measurement_details['w75'] = w75

        if w95 is not None:
            measurement_details['w95'] = w95
            
        if eid is not None:
            measurement_details['eid'] = eid

        self.measurements.append(measurement_details)

    def get_measurement_count(self):
        return len(self.measurements)

    def get_json(self):

        #if len(self.measurements) <= 0:
            #return None
        if (self.animal is not None):
            json_list = {'farmId':self.animal.farm_id,
                     'animalId': self.animal.id,
                     'algorithmId': self.algorithm.id,
                     'userId': self.user.id,
                     'measurements': self.measurements}
        else:
            json_list = {'farmId':self.farm_id,
                     'algorithmId': self.algorithm.id,
                     'userId': self.user.id,
                     'measurements': self.measurements}

        return json_list