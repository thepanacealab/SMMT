# Social Media Mining Toolkit - Data Annotation and Standardization Tools

## Utilities available:


**create_dictionary.py** This utility will create a dictionary that is compatible with the annotator (SMMT_NER_basic.py) and separator (separate_tweets.py) in the Social Media Mining Toolkit. This utility takes a downloaded dictionary from BioTermHub (https://pub.cl.uzh.ch/projects/ontogene/biotermhub/) and creates a dictionary that can be used with other utilities. The output of this program is outputfile.tsv, with the format -  termId TAB Term

| Arguments    | Description | Required |
| ------------- | ------------- | ------------- |
| i  | input text file name   | FILE_NAME of the downloaded BioTermHub dictionary  | Yes |
| o  | output file name  | Dictionary compatible with Social Media Mining Toolkit | Yes |


```
Usage : python create_dictionary.py -i uberon.tsv -o newuberon_dict.tsv
```


**separate_tweets.py** This utility separates Tweet json objects from a file of twitter json objects (obtained by hydrating tweets) using a dictionary. The input for this utlity is a json file with one json object per line. This program extracts the tweet text from the json object and uses the dictionary to identify the presence of dictionary. If there is a match, the tweet object is written to the output file. The output file consists of all such separated Tweet Json objects.

| Arguments     | Description | Required |
| ------------- | ------------- | ------------- |
| i  | input text file name   |   | Yes
| o  | output file name  |  | Yes |
| d | dictionary file name | Yes |
| t | no of threads (default is set to 1) | No |
| v | verbose – which gives all details of the program – total no of tweets processed, no of tweets separated, counts for each term saved in a csv file, total time taken to run the program | No |
| l | language | default set to English, but can take other languages “en” , “es”. | No |

How to run separate_tweets.py for obtaining spanish tweets:
```
python separate_tweets.py -i inputfile.json -d dictionary_file.tsv -o outputfile.tsv -l es -v y
```

**SMMT_NER_basic.py** This utility will annotate tweets in a given TSV file (TSV_source.tsv) with format tweetID tab Text, with a given dictionary dictionary_file.txt - with format termID TAB termString. The output can be obtained in 3 different formats. 

**Format compatible with Brat tool (https://brat.nlplab.org/manual.html)**
 - The output file consists of Textannotation TAB TermId TAB startSpan TAB endSpan. 
 - The annotated output file must be saved with an extension ".ann".
 - To use the Brat Visualization tool, annotation file and Text file (file with only one tweet Text per line) must be uploaded.

**Format compatible with TextAE and PubAnnotation (https://textae.pubannotation.org/)**
- The output file consists of one Json object per line. 
- Each line of the output file must be considered as a separate document.  
- Open the output file, copy the first line and save it as a text file "anno1.txt"
- Open TextAE editor and import the anno1.txt for visualization. 
- The following image is an example of the visualization.

Example with 2 annotations in a single tweet
![TextAE and Pub Annotation Example](https://github.com/thepanacealab/SMMT/blob/master/data_annotationANDstandardization/2termsAE.PNG)

Example with 1 annotation in a single tweet
![TextAE and Pub Annotation Example](https://github.com/thepanacealab/SMMT/blob/master/data_annotationANDstandardization/singletermAE.PNG)


| Arguments     | Description | Required |
| ------------- | ------------- | ------------- |
| i  | input text file name   |   | Yes
| o  | output file name  |  | Yes | 
| f | format of the output <ul><li>-b : compatible with brat tool </li><li>-t : compatible with TextAE and PubAnnotation</li> <li>-g : generic format (default) with the format - tweetID TAB termID TAB startSpan TAB endSpan. </li></ul> | No. Default is set to generic |


How to run the dictionary based annotator:
```
python SMMT_NER_basic.py -i TSV_source_file.tsv -d dictionary_file.csv -o outputfile.ann -f b

python SMMT_NER_basic.py -i TSV_source_file.tsv -d dictionary_file.csv -o outputfile.json -f t
```
