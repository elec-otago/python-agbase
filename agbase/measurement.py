 # Agbase - Measurement Path
 # 
 # Copyright (c) 2015. Elec Research.
 # 
 # This Source Code Form is subject to the terms of the Mozilla Public
 # License, v. 2.0. If a copy of the MPL was not distributed with this
 # file, You can obtain one at http://mozilla.org/MPL/2.0/

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

class MeasurementAPI:
  
  def __init__(self, ab):
    self.ab = ab
    #self.measurement = Measurement
  '''
    Upload a single measurement model object
    TODO. This is not implemented.
  '''
  def upload_measurement(self, measurement_details):
    result = self.ab.api_call('post', 'measurements/', measurement_details)

    if result.status_code != 200:
      return None

    json_response = result.json()

    json_measurement = json_response[u'measurement']

    self.ab.log("Measurement Dump >>> " + json.dumps(json_response))

    result_measurement = Measurement(None)

    result_measurement.init_with_json(json_measurement)

    return result_measurement

  def create_measurement(self, animal, algorithm, user, time_stamp, w05, w25, w50, w75, w95, comment):
    m = Measurement(None).to_json_animal(animal,algorithm,user,time_stamp, w05, w25, w50, w75, w95, comment)
    return self.upload_measurement(m)

  def create_measurement_for_eid(self, eid, farm, algorithm, user, time_stamp, w05, w25, w50, w75, w95, comment):
    m = Measurement(None).to_json_eid(eid,farm,algorithm,user,time_stamp, w05, w25, w50, w75, w95, comment)
    return self.upload_measurement(m)


  def remove_measurement(self, measurement):
    result = self.ab.api_call('delete', 'measurements/{}'.format(measurement.id))

    json_response = result.json()

    self.ab.log("Measurement Dump >>> " + json.dumps(json_response))

    if result.status_code != 200:
      return False

    return True


  def get_measurements_for_animal(self, animal, algorithm=None):
    params = {'animal': animal.id}

    if algorithm is not None:
      params['algorithm'] = algorithm

    result = self.ab.api_call('get', 'measurements/', None, params)

    if result.status_code != 200:
      return None

    json_response = result.json()

    self.ab.log("Measurement Dump >>> " + json.dumps(json_response))

    measurements = []

    for json_measurement in json_measurements:

      new_measurement = Measurement(None)
      new_measurement.init_with_json(json_measurement)
      measurements.append(new_measurement)

    return measurements


  def create_bulk_measurement_upload_list(self, animal, algorithm, user):
    return MeasurementList(animal, algorithm, user)


  def upload_measurement_list(self, measurement_list):

    result = self.ab.api_call('post', 'measurements/', measurement_list.get_json())

    if result.status_code != 200:
      return None

    return True
