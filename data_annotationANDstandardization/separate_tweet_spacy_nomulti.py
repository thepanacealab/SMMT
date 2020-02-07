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

import json
import time
import csv
import argparse
import datetime
import spacy
import os
import sys
import threading
import tarfile
import bz2
import glob
from bz2 import BZ2File
from xtract import xtract
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span

drugsList=[]
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--drugdictionary", help="Drug dictionary file with extension")
    parser.add_argument("-o", "--outputfile", help="Output file name with extension", required = False, default= "")
    parser.add_argument("-i", "--inputfile", help="Input file name with extension")
   
    args = parser.parse_args()
    if args.drugdictionary is None or args.inputfile is None:
        parser.error("please add necessary arguments")
    
    starttime = datetime.datetime.now()
    
    print(starttime)
    with open(args.drugdictionary) as f:
        reader = csv.reader(f, delimiter=",", quotechar="\"")
        next(reader)
        for drugRow in reader:
            drugsList.append(drugRow[1].lower())
    print("completed loading drug dictionary")
    nlp = spacy.load('en_core_web_sm',disable=['ner', "tagger"])
    drugPatterns = [nlp(drug) for drug in drugsList]  # process each word to create phrase pattern
    matcher = PhraseMatcher(nlp.vocab)
    matcher.add('DRUG', None, *drugPatterns)  # add patterns to matcher
    fO = open(args.outputfile, "w", encoding="utf-8")
    
    with open(args.inputfile, 'r') as f:
        cnt = 0
        for line in f:
            if line.strip().startswith('{'):
                    cnt += 1
                    tweet = json.loads(line)
                    if 'lang' in tweet and str(tweet["lang"]) == "en" and 'retweeted_status' not in tweet:
                        try:
                            tweetText = str(tweet["full_text"]).lower()
                        except:
                            tweetText = 'NULL'
                        doc = nlp(tweetText)
                        #print(tweetText)
                        matches = matcher(doc)                    
                        if len(matches) > 0:
                            fO.write(str(line))
        print(cnt)
        lasttime = datetime.datetime.now()
        stoptime = lasttime - starttime
        print(stoptime)
        fO.close()
# main invoked here    
main()
