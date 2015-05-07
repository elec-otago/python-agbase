import agbase_config as config
from models import *
from measurement_list import *

import requests
import json
import datetime
import urllib
import os

if os.getenv('MOOGLE_RUNNING_UNIT_TESTS', '0') == '1':
  # disable warnings about unverified https connections
  requests.packages.urllib3.disable_warnings()

__author__ = 'mark'


class AgBase:
  def __init__(self):
    self.agbase_api_url = None
    self.currentUser = ""
    self.currentPwd = ""
    self.session = requests.Session()
    self.session.headers.update({'content-type': 'application/json'})
    self.session.verify = config.defaultSigning
    self.authenticationTime = 0
    self.logging = False


  def __agbase_log(self, string):
    if self.logging is True:
      print("-- AgBase: {}".format(string))


  def api_call(self, http_verb, route, data=None, query_params=None):

    self.__agbase_log("API call of type {} to {}".format(http_verb,route))

    authenticated = True

    expiry_time = self.authenticationTime + datetime.timedelta(minutes=config.token_time_out)

    if self.authenticationTime == 0 or datetime.datetime.now() > expiry_time:

      if self.authenticationTime != 0:
        self.__agbase_log('Token Expired - reauthenticating')

      authenticated = self.__auth_user(self.currentUser, self.currentPwd)

    if not authenticated:
      return 0

    http_call = getattr(self.session, http_verb)

    if data is None and query_params is None:
      response = http_call(self.agbase_api_url + route)
    elif data is None and query_params is not None:
      response = http_call(self.agbase_api_url + route, params=query_params)
    elif query_params is None and data is not None:
      response = http_call(self.agbase_api_url + route, data=json.dumps(data))
    else:
      response = http_call(self.agbase_api_url + route, params=query_params, data=json.dumps(data))

    if response.status_code is not 200:
      print response.content

    return response


  def __auth_user(self, email, pwd):

    self.__agbase_log("Authenticating User")

    user_details = {"email": email, "password": pwd}

    post_response = self.session.post(self.agbase_api_url + "auth/", data=json.dumps(user_details))

    if post_response.status_code != 200:
      self.__agbase_log("Authentication Failed!")
      return None

    json_response = post_response.json()

    self.session.headers.update({'Authorization': 'Bearer ' + json_response[u'token']})

    self.authenticationTime = datetime.datetime.now()

    json_user = json_response[u'user']

    self.__agbase_log("Authenticated user {}!".format(json_user[u'email']))

    return User(json_user[u'firstName'], json_user[u'lastName'], json_user[u'email'], json_user[u'id'])


  def connect(self, email, pwd, agbase_api):
    self.currentUser = email
    self.currentPwd = pwd
    self.agbase_api_url = agbase_api

    return self.__auth_user(email, pwd)


  def set_logging_on(self, is_on):
    self.logging = is_on

    if is_on is True:
      self.__agbase_log("AgBase Logging Enabled!")


  #Requires current user to have admin rights
  def get_roles(self):

    result = self.__api_call('get', 'farm-roles/')

    if result.status_code != 200:
      return None

    json_response = result.json()

    json_roles = json_response[u'roles']

    roles = []

    for json_role in json_roles:
      roles.append(Role(json_role[u'name'], json_role[u'id']))

    return roles


  #Requires current user to have admin rights
  def create_user(self, first_name, last_name, email, password, role):

    user_details = {'firstName': first_name, 'lastName': last_name, 'email': email, 'password': password, 'roleId': role.id}

    result = self.__api_call('post', 'users/', user_details)

    if result.status_code != 200:
      return None

    json_response = result.json()

    json_user = json_response[u'user']

    self.__agbase_log(json_response[u'message'])

    return User(json_user[u'firstName'], json_user[u'lastName'], json_user[u'email'], json_user[u'id'])


  #Requires current user to have admin rights
  def remove_user(self, user):
    result = self.__api_call('delete', 'users/{}'.format(user.id))

    json_response = result.json()

    self.__agbase_log(json_response[u'message'])

    if result.status_code != 200:
      return False

    return True


  #Requires current user to have admin rights to access all users. Any user can see other users in their farm
  def get_users(self, farm=None):

    params = None

    if farm is not None:
      params = {'farm': farm.id}

    result = self.__api_call('get', 'users/', None, params)

    if result.status_code != 200:
      return None

    json_response = result.json()

    json_users = json_response[u'users']

    users = []

    for json_user in json_users:
      users.append(User(json_user[u'firstName'], json_user[u'lastName'], json_user[u'email'], json_user[u'id']))

    return users

