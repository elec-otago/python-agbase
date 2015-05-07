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


class MeasurementCategoryAPI:
  def __init__(self, ab):
    self.ab = ab
    
  def create_measurement_category(self, name):

    result = self.ab.api_call(self,'post', 'measurement-categories/', {'name': name})

    if result.status_code != 200:
      return None

    json_response = result.json()

    json_category = json_response[u'category']

    self.ab.__agbase_log(json_response[u'message'])

    return MeasurementCategory(json_category[u'name'], json_category[u'id'])


  def remove_measurement_category(self, category):
    result = self.ab.api_call(self,'delete', 'measurement-categories/{}'.format(category.id))

    json_response = result.json()

    self.ab.__agbase_log(json_response[u'message'])

    if result.status_code != 200:
      return False

    return True


  def get_measurement_categories(self):

    result = self.ab.api_call(self,'get', 'measurement-categories/')

    if result.status_code != 200:
      return None

    json_response = result.json()

    json_categories = json_response[u'categories']

    categories = []

    for json_category in json_categories:
      categories.append(MeasurementCategory(json_category[u'name'], json_category[u'id']))

    return categories


  def get_measurement_category(self, categoryId):
    result = self.ab.api_call(self,'get', 'measurement-categories/{}'.format(categoryId))

    if result.status_code != 200:
      return None

    json_category = result.json()[u'category']

    return MeasurementCategory(json_category[u'name'], json_category[u'id'])
