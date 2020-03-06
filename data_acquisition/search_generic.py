#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#   /$$$$$$  /$$      /$$ /$$      /$$ /$$$$$$$$
#  /$$__  $$| $$$    /$$$| $$$    /$$$|__  $$__/
# | $$  \__/| $$$$  /$$$$| $$$$  /$$$$   | $$   
# |  $$$$$$ | $$ $$/$$ $$| $$ $$/$$ $$   | $$   
#  \____  $$| $$  $$$| $$| $$  $$$| $$   | $$   
#  /$$  \ $$| $$\  $ | $$| $$\  $ | $$   | $$   
# |  $$$$$$/| $$ \/  | $$| $$ \/  | $$   | $$   
#  \______/ |__/     |__/|__/     |__/   |__/  
#
#
# Developed during Biomedical Hackathon 6 - http://blah6.linkedannotation.org/
# Authors: Ramya Tekumalla, Javad Asl, Juan M. Banda
# Contributors: Kevin B. Cohen, Joanthan Lucero

try:
    import json
except ImportError:
    import simplejson as json
#import urllib2
import urllib
import codecs
import time
import datetime
import os
import random
import time
import tweepy
from tweepy.parsers import RawParser
import sys
import argparse
from auth import TwitterAuth

def logPrint(s, fhLog):
	fhLog.write("%s\n"%s)
	print(s)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--searchterm", help="Search terms separated by comma.")
	parser.add_argument("-n", "--resultslimit", help="Total number of results the search should be limited to.")
	args = parser.parse_args()
	#only search term arugment is required
	if args.searchterm is None:
		parser.error("please add search term argument")

	fhLog = codecs.open("LOG.txt",'a','UTF-8')
	
	#Update this line with the terms you want to search for
	terms = list(args.searchterm.split(','))

	auth = tweepy.OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
	auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)

	api = tweepy.API(auth_handler=auth, parser=tweepy.parsers.JSONParser())

	

	termCnt=0
	for term in terms:
		termCnt+=1
		logPrint("Getting term %s (%s of %s)"%(term,termCnt,len(terms)), fhLog)
		fh=open(term + ".json", "w")
		#this line determines how many remaining results should be fetched
		#if there is no results limit argumemt keep getting 100 results at a time. 
		if args.resultslimit is None:
			resultsLimit = 100
		else:
			resultsLimit = int(args.resultslimit)
		
		remainingCount = resultsLimit
		while remainingCount > 0:
			try:
				if remainingCount >= 100:
					searchCount = 100
				else:
					searchCount = remainingCount
				result=api.search(count=searchCount,q=term,result_type="recent")
				limitS=len(result['statuses'])
				for i in range(0,limitS):
					fh.write(json.dumps(result['statuses'][i]) + "\n")
				if "statuses" in result and len(result["statuses"])>0:
					logPrint("There are %s results."%len(result["statuses"]), fhLog)
				remainingCount = resultsLimit if args.resultslimit is None else (remainingCount - 100)
				if remainingCount > 0:
					time.sleep(5)
			except:
				remainingCount = 0
		fh.close()

	logPrint("\nDONE! Completed Successfully", fhLog)
	fhLog.close()

main()
