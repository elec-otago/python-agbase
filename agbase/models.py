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
    
    def to_json(self):
        return {'name':self.name,'id':self.id}

class Algorithm:

    def __init__(self):
        self.name = ""
        self.id = -1
        self.category_id  = -1
        
    def init_with_json(self,algorithm_json):
        self.name = algorithm_json[u'name']
        self.id = algorithm_json[u'id']
        print algorithm_json
        if hasattr(algorithm_json,u'measurementCategoryId'):
            self.category_id  = algorithm_json[u'measurementCategoryId'] 

    def to_json(self):
        algorithm_json = {}
        algorithm_json[u'name'] = self.name
        algorithm_json[u'id'] = self.id
        algorithm_json[u'measurementCategoryId'] = self.category_id 
        return algorithm_json
        
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

    def to_json(self):
        return {'name':self.name,'id':self.id}

class Herd:

    def __init__(self, name, id=-1, farm_id=-1):
        self.name = name
        self.farm_id = farm_id
        self.id = id
    
    def to_json(self):
        return {'name':self.name, 'farm_id':self.farm_id, 'id':self.id}
import json
class Measurement:

    def __init__(self, median):
        self.id = -1
        self.w05 = 0
        self.w25 = 0
        self.w50 = 0
        self.w75 = 0
        self.w95 = 0
        self.time_stamp = None
        self.comment = ""
        self.user_id = -1
        self.algorithm_id = -1
        self.animal_id = -1
        self.animal = None

    def init_with_json(self, json_measurement):
        self.id = json_measurement[u'id']
        self.w05 = json_float(json_measurement[u'w05'])
        self.w25 = json_float(json_measurement[u'w25'])
        self.w50 = json_float(json_measurement[u'w50'])
        self.w75 = json_float(json_measurement[u'w75'])
        self.w95 = json_float(json_measurement[u'w95'])
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
            measurement_details['w05'] = w05
        
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
    
        print measurement_details
        return measurement_details

    def to_json_animal(self, animal, algorithm, user, time_stamp, w05, w25, w50, w75, w95, comment ):
        measurement_details = {'animalId':animal.id}
        return self.to_json(measurement_details, animal.farm_id, algorithm, user, time_stamp, w05, w25, w50, w75, w95, comment)
    
    
    def to_json_eid(self, animalEid, farm, algorithm, user, time_stamp, w05, w25, w50, w75, w95, comment ):
        measurement_details = {'eid':animalEid}
        return self.to_json(measurement_details,farm.id, algorithm, user, time_stamp, w05, w25, w50, w75, w95, comment )

    def __str__(self):
        return "%s %f, %s," % (self.animal_id,self.w50,self.time_stamp)
    
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
        r["animal"] = None
        if self.animal is not None:
            r["animal"] = self.animal.__repr__()
        return r


class Animal:

    def __init__(self, id=-1, eid="", vid="", herd_id=-1, farm_id=-1):

        self.id = id
        self.eid = eid
        self.vid = vid
        self.herd_id = herd_id
        self.farm_id = farm_id
        
    def init_with_json(self,json_animal):
        self.id = json_animal[u'id']
        self.eid = json_animal[u'eid']
        self.vid = json_animal[u'vid']
        self.farmId = json_animal[u'farmId']
        self.herdId = json_animal[u'herdId']
        
    def __repr__(self):
        r = {}
        r["id"] = self.id
        r["eid"] = self.eid
        r["vid"] = self.vid
        r["farmId"] = self.farm_id
        r["herdId"] = self.herd_id
        return r
    
    def __str__(self):
        return json.dumps(self.__repr__())