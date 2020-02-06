#!/usr/bin/env python
# ███████╗ ██████╗  ██████╗██╗ █████╗ ██╗         ███╗   ███╗███████╗██████╗ ██╗ █████╗     ███╗   ███╗██╗███╗   ██╗██╗███╗   ██╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗
# ██╔════╝██╔═══██╗██╔════╝██║██╔══██╗██║         ████╗ ████║██╔════╝██╔══██╗██║██╔══██╗    ████╗ ████║██║████╗  ██║██║████╗  ██║██╔════╝     ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝
# ███████╗██║   ██║██║     ██║███████║██║         ██╔████╔██║█████╗  ██║  ██║██║███████║    ██╔████╔██║██║██╔██╗ ██║██║██╔██╗ ██║██║  ███╗       ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║   
# ╚════██║██║   ██║██║     ██║██╔══██║██║         ██║╚██╔╝██║██╔══╝  ██║  ██║██║██╔══██║    ██║╚██╔╝██║██║██║╚██╗██║██║██║╚██╗██║██║   ██║       ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║   
# ███████║╚██████╔╝╚██████╗██║██║  ██║███████╗    ██║ ╚═╝ ██║███████╗██████╔╝██║██║  ██║    ██║ ╚═╝ ██║██║██║ ╚████║██║██║ ╚████║╚██████╔╝       ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║   
# ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   
                                                                                                                                                                                                   
# ██╗███████╗███╗   ███╗███╗   ███╗████████╗██╗                                                                                                                                                     
# ██╔╝██╔════╝████╗ ████║████╗ ████║╚══██╔══╝╚██╗                                                                                                                                                    
# ██║ ███████╗██╔████╔██║██╔████╔██║   ██║    ██║                                                                                                                                                    
# ██║ ╚════██║██║╚██╔╝██║██║╚██╔╝██║   ██║    ██║                                                                                                                                                    
# ╚██╗███████║██║ ╚═╝ ██║██║ ╚═╝ ██║   ██║   ██╔╝                                                                                                                                                    
# ╚═╝╚══════╝╚═╝     ╚═╝╚═╝     ╚═╝   ╚═╝   ╚═╝     
# 
# Developed during Biomedical Hackathon 6 - http://blah6.linkedannotation.org/
# Authors: Ramya Tekumalla, Javad Asl, Juan M. Banda
# Contributors:
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
    parser.add_argument("-d", "--dictionary", help="Dictionary file with extension")
    parser.add_argument("-o", "--outputfile", help="Output file name with extension", required = False, default= "")
    parser.add_argument("-i", "--inputfile", help="Input file name with extension")
   
    args = parser.parse_args()
    if args.dictionary is None or args.inputfile is None:
        parser.error("please add necessary arguments")
    
    starttime = datetime.datetime.now() 
    #print(starttime)
    with open(args.dictionary) as f:
        reader = csv.reader(f, delimiter=",", quotechar="\"")
        next(reader)
        for drugRow in reader:
            drugsList.append(drugRow[1].lower())
    print("completed loading dictionary")
    nlp = spacy.load('en_core_web_sm',disable=['ner', "tagger"])
    drugPatterns = [nlp(drug) for drug in drugsList]  # process each word to create phrase pattern
    matcher = PhraseMatcher(nlp.vocab)
    matcher.add('DRUG', None, *drugPatterns)  # add patterns to matcher
    fO = open(args.outputfile, "w", encoding="utf-8")
    
    with open(args.inputfile, 'r') as f:
        cnt = 0
        for line in f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                tweetId = row[0]
                userId = row[1]
                tweetText = row[2].lower()
                date = row[3]
                doc = nlp(tweetText)
                matches = matcher(doc)
                cnt += 1
                if len(matches) > 0:
                    fO.write(str(tweetId) + "\t" + str(userId) + "\t" + str(tweetText) + "\t" + str(date) + "\n")
        print("Total number of tweets separated " + str(cnt))
        lasttime = datetime.datetime.now()
        stoptime = lasttime - starttime
        print("Execution time " + str(stoptime))
        fO.close()
# main invoked here    
main()
