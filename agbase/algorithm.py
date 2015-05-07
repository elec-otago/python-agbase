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


class Algorithm(AgBase):  
  def __init__(self):
    AgBase.__init__(self)
    self.logging = False #= AgBase.logging
  def create_algorithm(self, name, measurement_category):

    result = AgBase.api_call(self,'post', 'algorithms/', {'name': name, 'measurementCategoryId': measurement_category.id})

    if result.status_code != 200:
      return None

    json_response = result.json()

    json_algorithm = json_response[u'algorithm']

    self.__agbase_log(json_response[u'message'])

    return Algorithm(json_algorithm[u'name'], json_algorithm[u'id'])


  def remove_algorithm(self, algorithm):
    result = AgBase.api_call(self,'delete', 'algorithms/{}'.format(algorithm.id))

    json_response = result.json()

    self.__agbase_log(json_response[u'message'])

    if result.status_code != 200:
      return False

    return True


  def get_algorithms(self, measurement_category=None):

    result = AgBase.api_call(self,'get', 'algorithms/')

    if result.status_code != 200:
      return None

    json_response = result.json()

    json_algorithms = json_response[u'algorithms']

    algorithms = []

    for json_algorithm in json_algorithms:
      algorithms.append(Algorithm(json_algorithm[u'name'],
                    json_algorithm[u'id'],
                    json_algorithm[u'MeasurementCategoryId']))

    return algorithms


  def get_algorithm(self, algorithmId):
    result = AgBase.api_call(self,'get', 'algorithms/{}'.format(algorithmId))

    if result.status_code != 200:
      return None

    json_algorithm = result.json()[u'algorithm']

    return Algorithm(json_algorithm[u'name'], json_algorithm[u'id'], json_algorithm[u'MeasurementCategoryId'])
