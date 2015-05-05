import psycopg2
import sys
import pprint
from agbase.agbase import AgBase
import time
import argparse
import math

__author__ = 'john'

class LocalToAgBase:
  recordLimit = -1
  def __init__(self):
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default=".agbase", help="AgBase Config File (username password e.t.c)")
    parser.add_argument('--user', required=True, help="AgBase Username")
    parser.add_argument('--passwd', required=True, help="AgBase Password")
    parser.add_argument('--server', default="https://agbase.elec.ac.nz/api/", help="AgBase Server")
    parser.add_argument('--print-weights' , action='store_true', help="Prints all the animals and their weights from the database")
    parser.add_argument('--upload-animals', action='store_true', help="Uploads all the animals from postgres to agbase")
    parser.add_argument('--upload-weights', action='store_true', help="Uploads all the weights from postgres to agbase")
    parser.add_argument('--print-animals', action='store_true', help="Print all animals from agbase")
    parser.add_argument('--limit', type=int, help="limit the number of animals that get added to agbase")
    parser.add_argument('--remove-animals', action='store_true', help="REMOVES ALL ANIMALS AND WEIGHTS")
    parser.add_argument('--db-host', default="postgres.elec.ac.nz", help="Local Database Host")
    parser.add_argument('--db-user', help="Local Database Username")
    parser.add_argument('--db-passwd', help="Local Database Password")
    
    args = parser.parse_args()
    self.testUser = args.user
    self.testPwd = args.passwd
    self.testServer = args.server

    conn = psycopg2.connect("dbname=moogle host=%s user=%s password=%s" % (args.db_host, args.db_user, args.db_passwd))
    cur = conn.cursor()  
    self.setup()
        
    if(args.limit):
      self.recordLimit = args.limit
      
    if(args.upload_animals):
      self.upLoadAnimalsToAgBase(cur)   
          
    if(args.upload_weights):
      self.uploadWeights(cur)
      
    if(args.print_weights):
      self.printWeightsFromAgBase()
    
    if(args.remove_animals):
      self.removeAllAnimals()
    
    if(args.print_animals):
      self.printAnimalsFromAgBase()
    #self.printWeightsFromAgBase()
    #self.printHerds(self.agbase.get_farm(31))
    cur.close()
    conn.close()
    
  def setup(self):
    print "prepering to transfer data from local database to AgBase ..."
    self.agbase = AgBase()    
    self.agbase.set_logging_on(True)
    self.user = self.agbase.connect(self.testUser, self.testPwd , self.testServer)
    if self.user is None:
      print("login failed")
      
  def removeAllAnimals(self):
    animals = self.agbase.get_animals(self.agbase.get_farm(31),None)
    for animal in animals:
      self.agbase.remove_animal(animal)
  
    
  def getWeights(self,cur,method_id,bridge):
    cur.execute("select distinct eid, date , w5 ,w50 ,w95 from weights join animal on (weights.animal_id = animal.id) join weighbridge on (weights.weighbridge_id = weighbridge.id) "+
                "where (weighbridge.name = '{}')and(weights.method_id = {});".format(bridge,method_id))
    return cur.fetchall()
  
  def getWeightsByEid(self,cur,method_id,bridge,eid):
    cur.execute("select distinct eid, date , w5 ,w50 ,w95 from weights join animal on (weights.animal_id = animal.id) join weighbridge on (weights.weighbridge_id = weighbridge.id) "+
                "where (weighbridge.name = '{}')and(weights.method_id = {})and (animal.eid = '{}');".format(bridge,method_id,eid))
    return cur.fetchall()
  
  def printWeights(self,cur,method_id,bridge):
    cur.execute("select distinct eid, date , w5 ,w50 ,w95 from weights join animal on (weights.animal_id = animal.id) join weighbridge on (weights.weighbridge_id = weighbridge.id)"+
                " where (weighbridge.name = '{}')and(weights.method_id = {});".format(bridge,method_id))
    pprint.pprint(cur.fetchall())
  
  
  def getMethod(self,cur,method_id):
    cur.execute("select * from method where method.id = %s;",([method_id]))
    return cur.fetchall()
    #self.upLoadToAgBase(cur.fetchall())
  
  def getHerds(self,farm):
    return self.agbase.get_herds(farm)
  
  def printHerds(self,farm):
    herds = self.agbase.get_herds(farm)
    for herd in herds:
      pprint.pprint("{} : {}".format(herd.name, herd.id))
  
  def getWeighBridges(self,cur,bridge):
    cur.execute("select * from weighbridge where (name = '{0}');".format(bridge))
    self.upLoadToAgBase(cur.fetchall())
    
  def getAnimals(self,cur,method_id,bridge):
    cur.execute('select distinct animal.eid, animal.id from animal join weights on(animal.id = weights.animal_id)join weighbridge on (weights.weighbridge_id = weighbridge.id) '+
        'where (weighbridge.name=%s)and(weights.method_id=%s) order by animal.id;', (bridge,method_id));
    return cur.fetchall()
  
  def printAnimals(self,cur,method_id,bridge):
    cur.execute('select distinct animal.eid, animal.id from animal join weights on(animal.id = weights.animal_id)join weighbridge on (weights.weighbridge_id = weighbridge.id) '+
        'where (weighbridge.name=%s)and(weights.method_id=%s) order by animal.id;', (bridge,method_id));
    pprint.pprint(cur.fetchall())
  
  def printAnimalsFromAgBase(self):
    farm = self.agbase.get_farms(self.user)
    animals = self.agbase.get_animals(farm)
    if animals is None:
      print"no animals in farm 31"
    
    for animal in animals:
      print'eid: {}'.format(animal.eid)
    print 'animals# {}'.format(len(animals))
  
  
  def printWeightsFromAgBase(self):
    farm = self.agbase.get_farm(31)
    animals = self.agbase.get_animals(farm)
    if animals is None:
      print"no animals in farm 31"
      
    i = 9
    for animal in animals:
      print'eid: {}'.format(animal.eid)
      animal_measurements = self.agbase.get_measurements_for_animal(animal)
      for weight in animal_measurements:
        print'        w5 {}, w50 {}, w95 {}'.format(weight.value1,weight.value2,weight.value3)
      print 'animals# {}'.format(len(animals))
    
  def upLoadToAgBase(self,cur): # ul = upload = stuff to put up to server
    cur.execute('select method_id from score order by cprs;')
    method_id = cur.fetchone()[0]
    algName = self.getMethod(cur,method_id)[0][1]
    
    cat = self.agbase.get_measurement_category(27)
    alg = self.agbase.create_algorithm(algName, cat)
    
    farm = self.agbase.get_farm(31)
    animals = self.getWeights(cur,method_id,"taieri")
    pprint.pprint(animals)
    for animal in animals:                   #eid                            #date            w5       w50       w95
      self.agbase.create_measurement_for_eid(animal[0], farm, alg, self.user, str(animal[1]),animal[2],animal[3],animal[4])
      
      
  def uploadWeights(self,cur):
    cur.execute('select method_id from score order by cprs;')
    method_id = cur.fetchone()[0]
    algName = self.getMethod(cur,method_id)[0][1]
    cat = self.agbase.create_measurement_category("Weight")
    cats = self.agbase.get_measurement_categories()
    for ccat in cats:
      pprint.pprint("{} {}".format(ccat.name,ccat.id))
      
    alg = self.agbase.create_algorithm(algName, cat)  
    
    farm = self.agbase.create_farm("Liquid Calcium")
    animals = self.agbase.get_animals(farm)
    amax = len(animals)
    acount = 0
    
    for animal in animals:
      if animal.eid != "":
        weights = self.getWeightsByEid(cur,method_id,"taieri",animal.eid)
        acount += 1
        print("animals {} / {}".format(acount,amax))
        wmax = len(weights)
        wcount = 0
      
        #make new animal_measurements      
        measurement_list = self.agbase.create_bulk_measurement_upload_list(animal, alg, self.user)
        for weight in weights:
          w = list(weight)
          wcount += 1
          print("measurement {} / {}".format(wcount,wmax))
          #self.agbase.create_measurement(animal, alg, self.user, str(w[1]),w[2],w[3],w[4])
          if math.isnan(w[2]):
            w[2] = None
          if math.isnan(w[3]):
            w[3] = None
          if math.isnan(w[4]):
            w[4] = None
          print "weight: {}".format(w[2])
          measurement_list.add_measurement(time.strftime(str(w[1])), w[2], w[3], w[4])
          
        success = self.agbase.upload_measurement_list(measurement_list)
    
  
  def upLoadAnimalsToAgBase(self,cur): # ul = upload = stuff to put up to server
    cur.execute('select method_id from score order by cprs;')
    method_id = cur.fetchone()[0]
    farm = self.agbase.create_farm("Liquid Calcium")
    herd = self.agbase.create_herd(farm, "Herd 1")
    animals = self.getAnimals(cur,method_id,"taieri")
    pprint.pprint(animals)
    count = 0
    minimum = 51
    for animal in animals:
      print "count: {}/{}".format(count,len(animals))
      count += 1
      if count >= minimum:
        self.agbase.create_animal(farm,animal[0])
        print "farm: {}, animal: {}".format(farm, animal)
        
      if count == self.recordLimit:
        break
       
    mAnimals = self.agbase.get_animals(farm)
    
    pprint.pprint(mAnimals)
    
    for animal in mAnimals:
      self.agbase.set_animal_herd(animal,herd)
        
        

if __name__ == '__main__':
  x = LocalToAgBase()





