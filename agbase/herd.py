 # Agbase - Herd Path
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


class HerdAPI:
  def __init__(self, ab):
    self.ab = ab
    
  def create_herd(self, farm, name):
    result = self.ab.api_call('post', 'herds/', {'name': name, 'farmId': farm.id})

    if result.status_code != 200:
      return None

    self.ab.log(result.json()[u'message'])

    json_response = result.json()[u'herd']

    return Herd(json_response[u'name'], json_response[u'id'], json_response[u'farmId'])


  def remove_herd(self, herd):
    result = self.ab.api_call('delete','herds/{}'.format(herd.id))

    self.ab.log(result.json()[u'message'])

    if result.status_code != 200:
      return False

    return True


  def get_herds(self, farm=None):

    params = None

    if farm is not None:
      params = {'farm': farm.id}

    result = self.ab.api_call('get', 'herds/', None, params)

    if result.status_code != 200:
      return None

    json_response = result.json()

    json_herds = json_response[u'herds']

    herds = []

    for json_herd in json_herds:
      herds.append(Herd(json_herd[u'name'], json_herd[u'id']))

    return herds

