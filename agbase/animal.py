 # Agbase - Animal Path
 # 
 # Copyright (c) 2015. Elec Research.
 # 
 # This Source Code Form is subject to the terms of the Mozilla Public
 # License, v. 2.0. If a copy of the MPL was not distributed with this
 # file, You can obtain one at http://mozilla.org/MPL/2.0/

import agbase_config as config
from models import *
from agbase import AgBase
import requests
import json
import datetime
import os

if os.getenv('MOOGLE_RUNNING_UNIT_TESTS', '0') == '1':
# disable warnings about unverified https connections
    requests.packages.urllib3.disable_warnings()

__author__ = 'John'


class AnimalAPI:
  
    def __init__(self, ab):
      self.ab = ab
      
    def create_animal(self, farm, eid, vid=None, herd=None):
        animal_details = {'farmId': farm.id, 'eid': eid}

        if vid is not None:
            animal_details['vid'] = vid

        if herd is not None:
            animal_details['herdId'] = herd.id

        result = self.ab.api_call('post', 'animals/', animal_details)

        if result.status_code != 200:
            return None

        json_response = result.json()

        json_animal = json_response[u'animal']

        self.ab.log(json_response[u'message'])

        return Animal(json_animal[u'id'],
            json_animal[u'eid'],
            json_animal[u'vid'],
            json_animal[u'herdId'],
            json_animal[u'farmId'])


    def set_animal_herd(self, animal, herd):
        if herd.farm_id != animal.farm_id:
            self.ab.log("Cannot add animal to herd on different farm!")
            return False

        result = self.ab.api_call('put', 'animals/{}'.format(animal.id), {'herdId': herd.id})

        json_response = result.json()

        self.ab.log(json_response[u'message'])

        if result.status_code != 200:
            return False

        animal.herd_id = herd.id

        return True


    def remove_animal(self, animal):
        result = self.ab.api_call('delete', 'animals/{}'.format(animal.id))

        json_response = result.json()

        self.ab.log(json_response[u'message'])

        if result.status_code != 200:
            return False

        return True
      
    def get_animals(self, farm=None, herd=None):

        params = None

        
        if farm is not None:
            params = {'farm': farm.id}
            if herd is not None:
                params['herd'] = herd.id
        else:
            print "Must have a farm to get a herd"
            return
        
        print "----------------params-------------", params
        result = self.ab.api_call('get', 'animals/',None,params)

        if result.status_code != 200:
            return None

        json_response = result.json()

        json_animals = json_response[u'animals']

        animals = []

        for json_animal in json_animals:
            animals.append(Animal(json_animal[u'id'],
                    json_animal[u'eid'],
                    json_animal[u'vid'],
                    json_animal[u'herdId'],
                    json_animal[u'farmId']))

        return animals


    def get_animal_by_eid(self, farm, eid):

        params = {'farm': farm.id, 'eid': (eid)}

        result = self.ab.api_call('get', 'animals/', None, params)

        if result.status_code != 200:
          return None
        
        json_response = result.json()
        self.ab.log("get_animal_by_eid -> %s" % json_response)
        
        json_animals = json_response[u'animals']
        
        if (len(json_animals) == 0):
            return None
        
        json_animal = json_animals[0]   

        return Animal( json_animal[u'id'],
                json_animal[u'eid'],
                json_animal[u'vid'],
                json_animal[u'herdId'],
                json_animal[u'farmId'])


    '''
        Return an animal object or 'None' if no such animal exists.
    '''
    def get_animal_by_vid(self, farm, vid):

        params = {'farm': farm.id, 'vid': (str(vid))}

        result = self.ab.api_call('get', 'animals/', None, params)

        if result.status_code != 200:
            return None

        json_response = result.json()
        json_animals = json_response[u'animals']
        
        if (json_animals == []):
            return None
        
        json_animal = json_animals[0]


        return Animal( json_animal[u'id'],
                json_animal[u'eid'],
                json_animal[u'vid'],
                json_animal[u'herdId'],
                json_animal[u'farmId'])


    def update_animal_vid(self, animal, vid):

        result = self.ab.api_call('put', 'animals/{}'.format(animal.id), {'vid': str(vid)})

        json_response = result.json()

        self.ab.log(json_response[u'message'])

        if result.status_code != 200:
            return False

        animal.vid = vid

        return True

