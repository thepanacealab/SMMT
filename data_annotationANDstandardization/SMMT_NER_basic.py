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

from spacy.lang.en import English
from spacy.pipeline import EntityRuler
import csv
import spacy
import glob
import os
import argparse
import pickle

def tagged_docs(docs,name):
	counter = 0.0
	keys = set()
	for key in docs:
		if len(docs[key].ents) > 0:
			keys.add(key)
			counter = counter + 1
	print(name, counter,len(docs),counter/len(docs))
	return keys

parser = argparse.ArgumentParser()
   
parser.add_argument('-d', required=True)
parser.add_argument('-i', required=True)
parser.add_argument('-o', required=True)

args = parser.parse_args()
dictionary_filename = args.d
input_file = args.i
output_file = args.o

temp = open(dictionary_filename)
dictionary_file = csv.reader(temp, delimiter='\t')
patterns = []
i = 0
for product in dictionary_file:
	if i ==0:
		i = i +1
		continue
	patterns.append({"label":product[0],"pattern":product[1]})

temp.close()
#print(len(patterns))

nlp = English()
ruler = EntityRuler(nlp)

ruler.add_patterns(patterns)
nlp.add_pipe(ruler)

products_raw = open(input_file)
products = csv.reader(products_raw,delimiter='\t')
extended_docs={}
i = 0
for product in products:
	if i ==0:
		i = i +1
		continue
	ID = product[0]
	description = product[1].lower()
	desc = nlp(description)
	extended_docs[ID] = desc
	i = i+1
products_raw.close()


Dkeys = tagged_docs(extended_docs,'description')
#print(len(Dkeys))

f_output = open(output_file, 'w', newline='')
csv_output = csv.writer(f_output, delimiter='\t')
csv_output.writerow(['DocumentID', 'TermID', 'SpanStart','SpanEnd'])
for key in extended_docs:
	if len(extended_docs[key].ents) > 0:
		for ent in extended_docs[key].ents:
			csv_output.writerow([key,ent.label_, ent.start_char, ent.end_char])
del extended_docs
f_output.close()
