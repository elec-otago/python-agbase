__author__ = 'Tim Molteno, Mark Butler'


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

def json_float(x):
    if x == None:
      return float('NaN')
    return float(x)

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
        self.user_id = json_measurement[u'UserId']
        self.algorithm_id = json_measurement[u'AlgorithmId']
        self.animal_id = json_measurement[u'AnimalId']


    def to_json(self):
        # {'eid': eid, 'farmId': farm.id,'algorithmId': algorithm.id, 'userId': user.id, 'timeStamp': time_stamp, 'value1': value1}
        John to finish
        
        
    def __str__(self):
        return "%f, %f, %f, %f, %f" % (self.w05, self.w25, self.w50, self.w75, self.w95)

class Animal:

    def __init__(self, id=-1, eid="", vid="", herd_id=-1, farm_id=-1):

        self.id = id
        self.eid = eid
        self.vid = vid
        self.herd_id = herd_id
        self.farm_id = farm_id
