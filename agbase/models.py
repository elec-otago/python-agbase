 # Models for Agbase API Library
 # 
 # Copyright (c) 2015. Elec Research.
 # 
 # This Source Code Form is subject to the terms of the Mozilla Public
 # License, v. 2.0. If a copy of the MPL was not distributed with this
 # file, You can obtain one at http://mozilla.org/MPL/2.0/

__author__ = 'Tim Molteno, Mark Butler, John Harborne'

# Utility to create a float from json where NaN is returned when the object doesn't exist
def json_float(x):
    if x == None:
      return float('NaN')
    return float(x)


class MeasurementCategory:

    def __init__(self, name, id=-1):
        self.name = name
        self.id = id


class Algorithm:

    def __init__(self, name, id=-1, category_id=-1):
        self.name = name
        self.id = id
        self.category_id = category_id


class User:

    def __init__(self, first_name, last_name, email, id=-1):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.id = id


class Role:

    def __init__(self, name, id=-1):
        self.name = name
        self.id = id


class Farm:

    def __init__(self, name, id=-1):
        self.name = name
        self.id = id


class Herd:

    def __init__(self, name, id=-1, farm_id=-1):
        self.name = name
        self.farm_id = farm_id
        self.id = id

class Measurement:

    def __init__(self, median):
        self.id = -1
        self.w05 = 0
        self.w25 = 0
        self.w50 = median
        self.w75 = 0
        self.w95 = 0
        self.time_stamp = None
        self.comment = ""
        self.user_id = -1
        self.algorithm_id = -1
        self.animal_id = -1


    def init_with_json(self, json_measurement):
        self.id = json_measurement[u'id']
        self.w05 = json_float(json_measurement[u'value1'])
        self.w25 = json_float(json_measurement[u'value2'])
        self.w50 = json_float(json_measurement[u'value3'])
        self.w75 = json_float(json_measurement[u'value4'])
        self.w95 = json_float(json_measurement[u'value5'])
        self.time_stamp = json_measurement[u'timeStamp']
        self.comment = json_measurement[u'comment']
        self.user_id = json_measurement[u'userId']
        self.algorithm_id = json_measurement[u'algorithmId']
        self.animal_id = json_measurement[u'animalId']

    def to_json(self, measurement_details,farm_id,algorithm, user, time_stamp, w05, w25, w50, w75, w95, comment):
        measurement_details['farmId'] = farm_id
        measurement_details['algorithmId'] = algorithm.id
        measurement_details['userId'] = user.id
        measurement_details['timeStamp'] = time_stamp
        
        if(w05 is  None and w25 is  None and w50 is  None and w75 is  None and w95 is  None):
            print "w:",w05,w25,w50,w75,w95
            print "w05,w25,w50,w75,w95 are all null"
            return
        
        if w05 is not None:
            measurement_details['value1'] = w05
        
        if w25 is not None:
            measurement_details['value2'] = w25

        if w50 is not None:
            measurement_details['value3'] = w50

        if w75 is not None:
            measurement_details['value4'] = w75

        if w95 is not None:
            measurement_details['value5'] = w95

        if comment is not None:
            measurement_details['comment'] = comment
    
        print measurement_details
        return measurement_details

    def to_json_animal(self, animal, algorithm, user, time_stamp, w05, w25, w50, w75, w95, comment ):
        measurement_details = {'animalId':animal.id}
        return self.to_json(measurement_details, animal.farm_id, algorithm, user, time_stamp, w05, w25, w50, w75, w95, comment)
    
    
    def to_json_eid(self, animalEid, farm, algorithm, user, time_stamp, w05, w25, w50, w75, w95, comment ):
        measurement_details = {'eid':animalEid}
        return self.to_json(measurement_details,farm.id, algorithm, user, time_stamp, w05, w25, w50, w75, w95, comment )

    def __str__(self):
        return "%f, %f, %f, %f, %f" % (self.w05, self.w25, self.w50, self.w75, self.w95)
    
    def __repr__(self):
        r = {}
        r["id"] = self.id
        r["time_stamp"] = self.time_stamp
        r["comment"] = self.comment
        r["user_id"] = self.user_id
        r["algorithm_id"] = self.algorithm_id
        r["animal_id"] = self.animal_id
        r["w05"] = self.w05
        r["w25"] = self.w25
        r["w50"] = self.w50
        r["w75"] = self.w75
        r["w95"] = self.w95
        return r


class Animal:

    def __init__(self, id=-1, eid="", vid="", herd_id=-1, farm_id=-1):

        self.id = id
        self.eid = eid
        self.vid = vid
        self.herd_id = herd_id
        self.farm_id = farm_id
