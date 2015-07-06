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
    a = Algorithm()
    a.init_with_json(json_algorithm)
    print "a :::::::::::::::::::::::::::: ", a.to_json()
    return a


  def remove_algorithm(self, algorithm):
    result = self.ab.api_call('delete', 'algorithms/{}'.format(algorithm.id))

    json_response = result.json()

    self.ab.log(json_response[u'message'])

    if result.status_code != 200:
      return False

    return True


  def get_algorithms(self, measurement_category=None):
    params = {}
    if measurement_category is not None:
        params['category'] = measurement_category.id

    result = self.ab.api_call('get', 'algorithms/', None, params)

    if result.status_code != 200:
      return None

    json_response = result.json()

    json_algorithms = json_response[u'algorithms']

    algorithms = []

    for json_algorithm in json_algorithms:
      a = Algorithm()  
      a.init_with_json(json_algorithm)
      print ">>>>>>>for loop a>>>>> ", a.to_json() 
      algorithms.append(a)

    return algorithms


  def get_algorithm(self, name):
    result = self.ab.api_call('get', 'algorithms/', None, {"name":name})

    if result.status_code != 200:
      return None
    json_response = result.json()
    #self.ab.log("get_algorithm Dump >>> " + json.dumps(json_response))
    json_algorithm = result.json()[u'algorithms'][0]
    #self.ab.log("get_algorithm Dump >>> " + json.dumps(json_algorithm))
    a = Algorithm()
    a.init_with_json(json_algorithm)
    return a