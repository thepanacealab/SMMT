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

import tweepy
import json
import math
import glob
import csv
import zipfile
import zlib
import argparse
from tweepy import TweepError
from time import sleep


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--outputfile", help="Output file name with extension")
    parser.add_argument("-i", "--inputfile", help="Input file name with extension")

    args = parser.parse_args()
    if args.inputfile is None or args.outputfile is None:
        parser.error("please add necessary arguments")

    with open('api_keys.json') as f:
        keys = json.load(f)

    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    api = tweepy.API(auth)
    
    output_file = args.outputfile
    output_file_noformat = output_file.split(".",maxsplit=1)[0]
    print(output_file)
    output_file = '{}'.format(output_file)
    output_file_short = '{}_short.json'.format(output_file_noformat)
    compression = zipfile.ZIP_DEFLATED    
    ids = []
    
    with open(args.inputfile) as f:
        for line in f:
            ids.append(line.replace("\n", ""))
        print(ids)
        print(len(ids))

    print('total ids: {}'.format(len(ids)))

    start = 0
    end = 100
    limit = len(ids)
    i = int(math.ceil(float(limit) / 100))

    print('metadata collection complete')
    print('creating master json file')
    with open(output_file, 'w') as outfile:
        for go in range(i):
            print('currently getting {} - {}'.format(start, end))
            sleep(6)  # needed to prevent hitting API rate limit
            id_batch = ids[start:end]
            start += 100
            end += 100
            tweets = api.statuses_lookup(id_batch)
            for tweet in tweets:
                json.dump(tweet._json, outfile)
                outfile.write('\n')
        
    outfile.close()

    print('creating ziped master json file')
    zf = zipfile.ZipFile('{}.zip'.format(output_file_noformat), mode='w')
    zf.write(output_file, compress_type=compression)
    zf.close()


    def is_retweet(entry):
        return 'retweeted_status' in entry.keys()

    def get_source(entry):
        if '<' in entry["source"]:
            return entry["source"].split('>')[1].split('<')[0]
        else:
            return entry["source"]
    
    
    print('creating minimized json master file')
    with open(output_file_short, 'w') as outfile:
        with open(output_file) as json_data:
            for tweet in json_data:
                data = json.loads(tweet)            
                t = {
                    "created_at": data["created_at"],
                    "text": data["text"],
                    "in_reply_to_screen_name": data["in_reply_to_screen_name"],
                    "retweet_count": data["retweet_count"],
                    "favorite_count": data["favorite_count"],
                    "source": get_source(data),
                    "id_str": data["id_str"],
                    "is_retweet": is_retweet(data)
                }
                json.dump(t, outfile)
                outfile.write('\n')
        
    f = csv.writer(open('{}.csv'.format(output_file_noformat), 'w'))
    print('creating CSV version of minimized json master file') 
    fields = ["favorite_count", "source", "text", "in_reply_to_screen_name", "is_retweet", "created_at", "retweet_count", "id_str"]                
    f.writerow(fields)       
    with open(output_file_short) as master_file:
        for tweet in master_file:
            data = json.loads(tweet)            
            f.writerow([data["favorite_count"], data["source"], data["text"].encode('utf-8'), data["in_reply_to_screen_name"], data["is_retweet"], data["created_at"], data["retweet_count"], data["id_str"].encode('utf-8')])
    

# main invoked here    
main()