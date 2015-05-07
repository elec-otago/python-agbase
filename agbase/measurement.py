import agbase_config as config
from models import *
from measurement_list import *
from agbase import AgBase
import requests
import json
import datetime
import urllib
import os

if os.getenv('MOOGLE_RUNNING_UNIT_TESTS', '0') == '1':
  # disable warnings about unverified https connections
  requests.packages.urllib3.disable_warnings()

__author__ = 'mark'


class Measurement(AgBase):
  def __init__(self):
    AgBase.__init__(self)
    self.logging = False #= AgBase.logging
  '''
    Upload a single measurement model object
    TODO. This is not implemented.
  '''
  def upload_measurement(self, farm, measurement):
    
    measurement_details = measurement.to_json()
    # {'eid': eid, 'farmId': farm.id,'algorithmId': algorithm.id, 'userId': user.id, 'timeStamp': time_stamp, 'value1': value1}

    result = AgBase.api_call(self,'post', 'measurements/', measurement_details)

    if result.status_code != 200:
      return None

    json_response = result.json()

    json_measurement = json_response[u'measurement']

    self.__agbase_log(json_response[u'message'])

    result_measurement = Measurement()

    result_measurement.init_with_json(json_measurement)

    return result_measurement

  def __create_measurement_with_details(self, measurement_details, value2=None, value3=None, value4=None, value5=None, comment=None):

    if value2 is not None:
      measurement_details['value2'] = value2

    if value3 is not None:
      measurement_details['value3'] = value3

    if value4 is not None:
      measurement_details['value4'] = value4

    if value5 is not None:
      measurement_details['value5'] = value5

    if comment is not None:
      measurement_details['comment'] = comment

    result = AgBase.api_call(self,'post', 'measurements/', measurement_details)

    if result.status_code != 200:
      return None

    json_response = result.json()

    json_measurement = json_response[u'measurement']

    self.__agbase_log(json_response[u'message'])

    result_measurement = Measurement()

    result_measurement.init_with_json(json_measurement)

    return result_measurement


  def create_measurement(self, animal, algorithm, user, time_stamp, value1, value2=None, value3=None, value4=None, value5=None, comment=None):

    measurement_details = {'animalId': animal.id, 'algorithmId': algorithm.id, 'userId': user.id, 'timeStamp': time_stamp, 'value1': value1}

    return self.__create_measurement_with_details(measurement_details, value2, value3, value4, value5, comment)


  def create_measurement_for_eid(self, eid, farm, algorithm, user, time_stamp, value1, value2=None, value3=None, value4=None, value5=None, comment=None):

    measurement_details = {'eid': eid, 'farmId': farm.id,'algorithmId': algorithm.id, 'userId': user.id, 'timeStamp': time_stamp, 'value1': value1}

    return self.__create_measurement_with_details(measurement_details, value2, value3, value4, value5, comment)


  def remove_measurement(self, measurement):
    result = AgBase.api_call(self,'delete', 'measurements/{}'.format(measurement.id))

    json_response = result.json()

    self.__agbase_log(json_response[u'message'])

    if result.status_code != 200:
      return False

    return True


  def get_measurements_for_animal(self, animal, algorithm=None):
    params = {'animal': animal.id}

    if algorithm is not None:
      params['algorithm'] = algorithm

    result = AgBase.api_call(self,'get', 'measurements/', None, params)

    if result.status_code != 200:
      return None

    json_response = result.json()

    json_measurements = json_response[u'measurements']

    measurements = []

    for json_measurement in json_measurements:

      new_measurement = Measurement()
      new_measurement.init_with_json(json_measurement)
      measurements.append(new_measurement)

    return measurements


  def create_bulk_measurement_upload_list(self, animal, algorithm, user):
    return MeasurementList(animal, algorithm, user)


  def upload_measurement_list(self, measurement_list):

    result = AgBase.api_call(self,'post', 'measurements/', measurement_list.get_json())

    if result.status_code != 200:
      return None

    return True