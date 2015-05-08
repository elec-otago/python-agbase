 # Agbase API Library
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
import urllib
import os

if os.getenv('MOOGLE_RUNNING_UNIT_TESTS', '0') == '1':
  # disable warnings about unverified https connections
  requests.packages.urllib3.disable_warnings()

__author__ = 'John'


class FarmAPI:
  
  def __init__(self, ab):
    self.ab = ab
      
  def create_farm(self, name):
    result = self.ab.api_call('post', 'farms/', {'name': name})

    if result.status_code != 200:
      return None

    json_response = result.json()

    self.ab.log(json_response[u'message'])

    json_farm = json_response[u'farm']

    return Farm(json_farm[u'name'], json_farm[u'id'])


  def remove_farm(self, farm):
    result = self.ab.api_call('delete', 'farms/{}'.format(farm.id))

    self.ab.log(result.json()[u'message'])

    if result.status_code != 200:
      return False

    return True


  def get_farms(self, user=None):

    params = None

    if user is not None:
      params = {'user': user.id}

    result = self.ab.api_call('get','farms/', None, params )

    if result.status_code != 200:
      return None

    json_response = result.json()

    json_farms = json_response[u'farms']

    farms = []

    for json_farm in json_farms:
      farms.append(Farm(json_farm[u'name'], json_farm[u'id']))

    return farms


  def get_farm(self, farmId):
    result = self.ab.api_call('get', 'farms/{}'.format(farmId))

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

