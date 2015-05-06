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


class Farm(AgBase):  
  def create_farm(self, name):
    result = self.__api_call('post', 'farms/', {'name': name})

    if result.status_code != 200:
      return None

    json_response = result.json()

    self.__agbase_log(json_response[u'message'])

    json_farm = json_response[u'farm']

    return Farm(json_farm[u'name'], json_farm[u'id'])


  def remove_farm(self, farm):
    result = self.__api_call('delete', 'farms/{}'.format(farm.id))

    self.__agbase_log(result.json()[u'message'])

    if result.status_code != 200:
      return False

    return True


  def get_farms(self, user=None):

    params = None

    if user is not None:
      params = {'user': user.id}

    result = self.__api_call('get','farms/', None, params )

    if result.status_code != 200:
      return None

    json_response = result.json()

    json_farms = json_response[u'farms']

    farms = []

    for json_farm in json_farms:
      farms.append(Farm(json_farm[u'name'], json_farm[u'id']))

    return farms


  def get_farm(self, farmId):
    result = self.__api_call('get', 'farms/{}'.format(farmId))

    if result.status_code != 200:
      return None

    json_farm = result.json()[u'farm']

    return Farm(json_farm[u'name'], json_farm[u'id'])

  def get_farm_by_name(self, user, farmName):
    farms = self.get_farms(user)
    for f in farms:
      if (f.name == farmName):
        return f
    return None

