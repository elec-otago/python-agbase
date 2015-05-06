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


class AgBase.Herd:  
  def __init__(self):
      self.__api_call = AgBase.__api_call

  def create_herd(self, farm, name):
    result = self.__api_call('post', 'herds/', {'name': name, 'farmId': farm.id})

    if result.status_code != 200:
      return None

    self.__agbase_log(result.json()[u'message'])

    json_response = result.json()[u'herd']

    return Herd(json_response[u'name'], json_response[u'id'], json_response[u'FarmId'])


  def remove_herd(self, herd):
    result = self.__api_call('delete','herds/{}'.format(herd.id))

    self.__agbase_log(result.json()[u'message'])

    if result.status_code != 200:
      return False

    return True


  def get_herds(self, farm=None):

    params = None

    if farm is not None:
      params = {'farm': farm.id}

    result = self.__api_call('get', 'herds/', None, params)

    if result.status_code != 200:
      return None

    json_response = result.json()

    json_herds = json_response[u'herds']

    herds = []

    for json_herd in json_herds:
      herds.append(Herd(json_herd[u'name'], json_herd[u'id']))

    return herds

