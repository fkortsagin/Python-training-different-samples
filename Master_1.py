import re
import code
import sys
import os
import time 
import string
import time
import json
import requests
from pprint import pprint


'''
wrapper class for staging rest calls
'''
class StagingRest(object):
	def __init__(self):
		self.host = "https://keystone-staging.mwbsys.com"
		self.inpType = {'content-type': 'application/json','Authorization':'Token token="aKV2QeBV5QNvS-tLMrV_"'}
		self.timeout = 30
		self.base = "%s/api/v1" % self.host
		self.inst_base = "%s/installations" % self.base
		self.trials_base = "%s/trials" % self.base
		self.keys_base = "%s/keys" % self.base
		self.keygen_base = "%s/keygen" % self.base
	def postRest(self,_url,parm_dict,postName):
		#
		jrc = None
		post_json = json.dumps(parm_dict)
		print "=" * 70
		pprint ("*%s : Post the following data %s" % (postName,post_json))
		pprint ("to the following url %s" % _url)
		print "=" * 70
		#
		r = requests.post(_url,data=post_json, headers=self.inpType,timeout=self.timeout)
		
		try:
			jrc = json.loads(r.content)
			print "= %s JSON response object = " % postName + "=" * 60
			pprint(jrc)
			print "= /%s JSON response object = " % postName + "=" * 60 + "\n"
		except:
			print "--- probable issue with json return in %s  call" % postName
		return r,jrc
		
	def putRest(self,_url,parm_dict,putName):
		#
		jrc = None
		
		if parm_dict != None:
			post_json = json.dumps(parm_dict)
		else:
			post_json = None
			
		print "=" * 70
		pprint ("*%s : Put the following data %s" % (putName,post_json))
		pprint ("to the following url %s" % _url)
		print "=" * 70
		#
		r = requests.put(_url,data=post_json, headers=self.inpType,timeout=self.timeout)
		
		try:
			jrc = json.loads(r.content)
			print "= %s JSON response object = " % putName + "=" * 60
			pprint(jrc)
			print "= /%s JSON response object = " % putName + "=" * 60 + "\n"
		except:
			print "--- probable issue with json return in %s  call" % putName
		return r,jrc
		
	def deleteRest(self,_url,deleteName):
		#
		jrc = None   
		print "=" * 70
		pprint ("%s : Delete the following url %s" % (deleteName,_url) )
		print "=" * 70
		#	
		r = requests.delete(_url,data=None,headers=self.inpType,timeout=self.timeout)
		try:
			jrc = json.loads(r.content)
			print "= check JSON response object = " + "=" * 60
			pprint(jrc)
			print "= /check JSON response object = " + "=" * 60 + "\n"
		except:
			print "--- probable issue with json return in key call"
		return r,jrc
		
	def getRest(self,_url,getName):
		#
		jrc = None
		
		print "=" * 70
		pprint ("** %s get from following url %s" % (getName,_url))
		print "=" * 70
		r = requests.get(_url,headers=self.inpType,timeout=self.timeout)
		
		try:
			jrc = json.loads(r.content)
			print "= getEvent JSON response object = " + "=" * 60
			pprint(jrc)
			print "= /getEvent JSON response object = " + "=" * 60 + "\n"
		except:
			print "--- probable issue with json return in %s call" % getName
		return r,jrc
		
		
		
		
#
# basic functions to wrap the more usefull of rest calls
#
def bkpoint(msg=""):
	import code, sys
	
	# use exception trick to pick up the current frame
	try:
		raise None
	except:
		frame = sys.exc_info()[2].tb_frame.f_back
	
	# evaluate commands in current namespace
	namespace = frame.f_globals.copy()
	namespace.update(frame.f_locals)
	code.interact(banner="-%s>>" % msg, local=namespace)
	
	
# keygen
def keyGenLicenseGen(pdict):
	stg = StagingRest()
	_url = "%s/generate.json" % stg.keygen_base 
	return stg.postRest(_url,pdict,"keyGenLicenseGen")
	
	
# change activation date for activation_on_redeem
# there is another function for activation_on_purchase
def changeActDate(pdict):
	stg = StagingRest()
	lkey = pdict['key']
	eid  = pdict['entitlement_id']
	
	del(pdict['key'])
	del(pdict['entitlement_id'])
	_url =  "%s/%s/entitlements/%s/change_activation_date" % (stg.base,lkey,eid)
	return stg.postRest(_url,pdict,"changeActDate")
	
	
	
def blacklist(lkey):
	stg = StagingRest()
	_url = "%s/blacklist/%s" % (stg.keygen_base,lkey)
	return stg.putRest(_url,None,"blacklist")
	
	
	
def getEntitlements(lkey):
	stg = StagingRest()
	_url = "%s/%s/entitlements" % (stg.keys_base ,lkey)
	return stg.getRest(_url,"getEntitlements")
	
	
	
def retEntitlementsList(lkey):
	stg = StagingRest()
	ent_list = []
	r,jrc = getEntitlements(lkey)
	if jrc.has_key('entitlements'):
		for ent in jrc['entitlements']:
			ent_list.append(ent['id'])
	return ent_list
	
	
def delEntitlement(pdict):
	stg = StagingRest()
	lkey			= pdict['key']
	entitlement_id  = pdict['entitlement_id']
	_url = "%s/%s/entitlements/%s" % (stg.keys_base,lkey,entitlement_id)
	return stg.deleteRest(_url,"delEntitlement")
	
def delKey(lkey):
	stg = StagingRest()
	_url = "%s/%s" % (stg.keys_base,lkey)
	return stg.deleteRest(_url,"delKey")
	
def delEntitlementsAndLicense(lkey):
	elist  = retEntitlementsList(lkey)
	for ent_id in elist:
		r,jrc = delEntitlement({"key":lkey,"entitlement_id":ent_id})
	r,jrc = delKey(lkey)
	
# true or false
def setEntitlementsActive(lkey,value):
	stg = StagingRest()
	elist  = retEntitlementsList(lkey)
	for ent_id in elist:
		_url = "%s/%s/entitlements/%s" % (stg.keys_base ,lkey,ent_id)
		put_dict = {"key":lkey,'entitlement':{'entitlement_id':ent_id,"active":value}}
		r,jrc = stg.putRest(_url,put_dict,"setEntitlementsActive")
	return r,jrc   
	
# true or false
def setEntitlementsAbuse(lkey,value):
	stg = StagingRest()
	elist  = retEntitlementsList(lkey)
	for ent_id in elist:
		_url = "%s/%s/entitlements/%s" % (stg.keys_base ,lkey,ent_id)
		put_dict = {"key":lkey,'entitlement':{'entitlement_id':ent_id,"abused":value}}
		r,jrc = stg.putRest(_url,put_dict,"setEntitlementsActive")
	return r,jrc   
	
# Aaron MCNRF-W4ZHN-RGQK2-BXNRK == expire mbam-c 
# Noodle MCDMR-TTNXT-ZF7KJ-GCMVJ mbam-c not expired
# legacy  -- 7JH92-G66VP:YUBE-UPAX-BDL6-YB9Q   perpetual
# 
# Start HERE
#
if __name__== "__main__":
	key_gen_dict = {
	"key_format":"keystone",				   # keystone | legacy | amnesty (harmonize with key source as well unless you need amnesty key)
	"entitlement_attributes":[
	{"auto_renew":"no",						# yes | no
	"term_length":180,						 # in days
	"activation_type": "activation_on_redeem", # activation_on_redeem | activation_on_purchase ==> (activation date + term + 30 days   OR purchased_date + term + 30)
	"volume_purchased": 1000000,				   # number of seats
	"products": "mbam-c",					  # product code
	"term_type": "perpetual"}			   # subscription | perpetual | usage
	],
	# source is not used dont change it in fact its probably best to leave the key dictionary alone
	"key": {"source": "keystone", "transaction_source": "zuora"}
	}
	#
	# Generate the license, as per the above key_gen_dict directives
	#
	# r,jrc = keyGenLicenseGen( key_gen_dict )  
	# lkey = jrc['key']['license_key']
	# eid =  jrc['key']['entitlements'][0]['id']
	## r,jrc = blacklist(lkey)
	#
	#  Useful for changing the license.entitlement to expired
	#
	# change the activation date : yyyy-mm-dd for activated at
	# if you want to do some datetime math by subtracting days python has something for you
	#
	if 0:
		r,jrc = changeActDate({"key":lkey,"entitlement_id":eid,"activated_at":"2014-01-01"})
	
	#
	# activate/deactivate entitlements
	#
	if 0:
		# value = True or False , make sure you capitalize the first char
		# activates the entitlements for the license [default state] == True   , or deactivates == False
		r,jrc = setEntitlementsActive(lkey,False)  # deactivates
	
	
	# abused
	if 0:
		# value = True or False , make sure you capitalize the first char
		# mrks entitlements for the license as not abused [default state] == False or Abused == True
		setEntitlementsAbuse(lkey,True) #abuses
		
	'''
	if __name__== "__main__":
	
	lkey = 'MCGQ9-T9PMH-K64DT-T8WM6'
	'''
	
	#
	# blacklist the key .. cannot be undone
	#
	if 0:
		r,jrc = blacklist(lkey)
	
	# delete all entitlements and license
	if 0:
		delEntitlementsAndLicense(lkey)
	
		
	
	# list license entitlement	
	if 1:
		getEntitlements('7MT93:WDM7-35LM-XHP5-8QE0')
		