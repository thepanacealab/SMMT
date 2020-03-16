#!/usr/bin/env python
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
jsonFilesList = []
inputLineCounter = 0

# creates list of lists of json files to be processed in a thread and length of list is n.
def ChunkIt(a, n):  # n = number of items to be divided into
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

# separate tweets using drug dictionary for each thread
def ProcessFilesInThread(filesList, nlp, matcher, fO,lng):
    for file in filesList:
        with open(file, 'r') as f:
            for line in f:
                if line.strip().startswith('{'):
                    tweet = json.loads(line)
                    if 'lang' in tweet and str(tweet["lang"]) == lng  and 'retweeted_status' not in tweet:
                        try:
                            tweetText = str(tweet["text"]).lower()
                        except:
                            tweetText = 'NULL'
                        doc = nlp(tweetText)
                        matches = matcher(doc)                   
                        if len(matches) > 0:
                            fO.write(str(line))
    
# parses all the json files in a directory and add them to a list
def jsonParse(inputPath):
    jsonFiles = glob.glob(inputPath + '/**/*.json', recursive=True)
    for file in jsonFiles:
        with open(file) as f:
            global inputLineCounter
            inputLineCounter  = sum(1 for line in f)
        jsonFilesList.append(file)
    return jsonFilesList

# gives all the details when verbose is enabled. 
def drugcount(filename, nlp, matcher):
    fV = open("drugcounts.csv", "w", encoding="utf-8")
    outputLineCount = 0
    drugCount = {}
    with open(filename) as f:
        for line in f:
           if line.strip().startswith('{'):
               outputLineCount = outputLineCount + 1
               tweet = json.loads(line)
               tweetText = str(tweet["text"]).lower()
               doc = nlp(tweetText)
               matches = matcher(doc)                
               for match_id, start, end in matches:
                   span = doc[start : end]  # get the matched slice of the doc
                   if str(span) in drugCount:
                       drugCount [str(span)]+=1
                   else:
                       drugCount [str(span)]=1 
        sorted_by_value = sorted(drugCount.items(), key=lambda kv: kv[1], reverse = True)
        for i in sorted_by_value:
            fV.write(i[0] + "," + str(i[1]) + "\n")
        print("Total number of tweets processed - " + str(inputLineCounter))
        print("Total number of tweets separated using dictionary - " + str(outputLineCount))
        print("The counts of drugs for " +str(outputLineCount) + " are saved in drugcounts.csv")
        fV.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--drugdictionary", help="Drug dictionary file with extension")
    parser.add_argument("-o", "--outputfile", help="Output file name with extension")
    parser.add_argument("-i", "--inputfolder", help="Input file name with extension")
    parser.add_argument("-t", "--threadcount", help="Enter number of threads", required = False, default = 1 )
    parser.add_argument("-v", "--verbose", help="Enter number of threads", required = False)
    parser.add_argument("-l", "--language", help="Enter language: example - enter en for English", required = False, default= "en")

    

    args = parser.parse_args()
    if args.drugdictionary is None or args.inputfolder is None or args.outputfile is None:
        parser.error("please add necessary arguments")
        
    
    t = int (args.threadcount)
    lng = args.language
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

    jsonFilesList = jsonParse(args.inputfolder)   
    print("Completed parsing all the files and found " + str(len(jsonFilesList)) + " json files.")
    
    jsonFiles = list(ChunkIt(jsonFilesList, t))
    threads = []
    print("Initiating threads!!")
    for filesList in jsonFiles:
        threads.append(threading.Thread(target=ProcessFilesInThread, args=(filesList, nlp, matcher,fO,lng)))
        threads[-1].start()
    print("Created " + str(len(threads)) + " threads to process json files.")
    for t in threads:
        t.join()
    
    while True:
        currentThreads = [t for t in threads if t.is_alive()]
        if len(currentThreads) == 0:
            fO.close()    
            print("completed processing json files. Please check your output files!!")    
            if args.verbose is not None:
                drugcount(args.outputfile , nlp, matcher)
                stoptime = datetime.datetime.now()
                timedifference = stoptime - starttime
                print("Total time taken to process, separate and get counts of tweets - " + str(timedifference))
            break
    
# main invoked here    
main()