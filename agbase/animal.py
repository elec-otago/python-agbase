import agbase_config as config
from models import *
from agbase import AgBase
import requests
import json
import datetime
import urllib
import os

if os.getenv('MOOGLE_RUNNING_UNIT_TESTS', '0') == '1':
# disable warnings about unverified https connections
    requests.packages.urllib3.disable_warnings()

__author__ = 'John'


class Animal(AgBase):  
    def create_animal(self, farm, eid, vid=None, herd=None):
        animal_details = {'farmId': farm.id, 'eid': eid}

        if vid is not None:
            animal_details['vid'] = vid

        if herd is not None:
            animal_details['herdId'] = herd.id

        result = self.__api_call('post', 'animals/', animal_details)

        if result.status_code != 200:
            return None

        json_response = result.json()

        json_animal = json_response[u'animal']

        self.__agbase_log(json_response[u'message'])

        return Animal(json_animal[u'id'],
            json_animal[u'eid'],
            json_animal[u'vid'],
            json_animal[u'HerdId'],
            json_animal[u'FarmId'])


    def set_animal_herd(self, animal, herd):
        if herd.farm_id != animal.farm_id:
            self.__agbase_log("Cannot add animal to herd on different farm!")
            return False

        result = self.__api_call('put', 'animals/{}'.format(animal.id), {'herdId': herd.id})

        json_response = result.json()

        self.__agbase_log(json_response[u'message'])

        if result.status_code != 200:
            return False

        animal.herd_id = herd.id

        return True


    def remove_animal(self, animal):
        result = self.__api_call('delete', 'animals/{}'.format(animal.id))

        json_response = result.json()

        self.__agbase_log(json_response[u'message'])

        if result.status_code != 200:
            return False

        return True


    def get_animals(self, farm=None, herd=None):

        params = None

        if herd is not None:
            params = {'herd': herd.id}
        elif farm is not None:
            params = {'farm': farm.id}

        result = self.__api_call('get', 'animals/')

        if result.status_code != 200:
            return None

        json_response = result.json()

        json_animals = json_response[u'animals']

        animals = []

        for json_animal in json_animals:
            animals.append(Animal(json_animal[u'id'],
                    json_animal[u'eid'],
                    json_animal[u'vid'],
                    json_animal[u'HerdId'],
                    json_animal[u'FarmId']))

        return animals


    def get_animal_by_eid(self, farm, eid):

        params = {'farm': farm.id, 'eid': urllib.quote_plus(eid)}

        result = self.__api_call('get', 'animals/', None, params)

        if result.status_code != 200:
            json_animals = json_response[u'animals']
        
        json_response = result.json()
        
        if (len(json_animals) == 0):
            return None
        
        json_animal = json_animals[0]   

        return Animal( json_animal[u'id'],
                json_animal[u'eid'],
                json_animal[u'vid'],
                json_animal[u'HerdId'],
                json_animal[u'FarmId'])


    '''
        Return an animal object or 'None' if no such animal exists.
    '''
    def get_animal_by_vid(self, farm, vid):

        params = {'farm': farm.id, 'vid': urllib.quote_plus(str(vid))}

        result = self.__api_call('get', 'animals/', None, params)

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
                json_animal[u'HerdId'],
                json_animal[u'FarmId'])


    def update_animal_vid(self, animal, vid):

        result = self.__api_call('put', 'animals/{}'.format(animal.id), {'vid': str(vid)})

        json_response = result.json()

        self.__agbase_log(json_response[u'message'])

        if result.status_code != 200:
            return False

        animal.vid = vid

        return True

