 # Agbase - Algorithm Path
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


class AlgorithmAPI:  
  def __init__(self, ab):
    self.ab = ab
    
  def create_algorithm(self, name, measurement_category):

    result = self.ab.api_call('post', 'algorithms/', {'name': name, 'measurementCategoryId': measurement_category.id})

    if result.status_code != 200:
      return None

    json_response = result.json()

    json_algorithm = json_response[u'algorithm']

    self.ab.log(json_response[u'message'])

    return Algorithm(json_algorithm[u'name'], json_algorithm[u'id'])


  def remove_algorithm(self, algorithm):
    result = self.ab.api_call('delete', 'algorithms/{}'.format(algorithm.id))

    json_response = result.json()

    self.ab.log(json_response[u'message'])

    if result.status_code != 200:
      return False

    return True


  def get_algorithms(self, measurement_category=None):

    result = self.ab.api_call('get', 'algorithms/')

    if result.status_code != 200:
      return None

    json_response = result.json()

    json_algorithms = json_response[u'algorithms']

    algorithms = []

    for json_algorithm in json_algorithms:
      algorithms.append(Algorithm(json_algorithm[u'name'],
                    json_algorithm[u'id'],
                    json_algorithm[u'measurementCategoryId']))

    return algorithms


  def get_algorithm(self, algorithmId):
    result = self.ab.api_call('get', 'algorithms/{}'.format(algorithmId))

    if result.status_code != 200:
      return None

    json_algorithm = result.json()[u'algorithm']

    return Algorithm(json_algorithm[u'name'], json_algorithm[u'id'], json_algorithm[u'measurementCategoryId'])
