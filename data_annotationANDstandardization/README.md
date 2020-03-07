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

**SMMT_NER_basic.py** This utility will annotate tweets in a given TSV file (TSV_source.tsv) with format tweetID tab Text, with a given dictionary dictionary_file.txt - with format termID TAB termString. The output can be obtained in 4 different formats. 

**  Format compatible with Brat tool (https://brat.nlplab.org/manual.html) **
 - The output file consists of Textannotation TAB TermId TAB startSpan TAB endSpan. 
 - The annotated output file must be saved with an extension ".ann".
 - To use the Brat Visualization tool, annotation file and Text file (file with only one tweet Text per line) must be uploaded.

** Format compatible with TextAE and PubAnnotation (https://textae.pubannotation.org/) **
- The output file consists of Json object.
- To use the output file, open the text editor on TextAE and import the output file. 
- The following image is an example of the visualization.

** Format compatible with Colab notebook (https://colab.research.google.com/drive/1c_5JBJ7diMDeUVVxZG95_25bZ-u8ZIDZ) **
- The output file consists of Tweet Text and annotated Label.
- To use the output file, upload the output file on the colab notebook and keep running the notebook.

![TextAE and Pub Annotation Example](textAE.png)


| Arguments     | Description | Required |
| ------------- | ------------- | ------------- |
| i  | input text file name   |   | Yes
| o  | output file name  |  | Yes | 
| f | format of the output <ul><li>-b : compatible with brat tool </li><li>-t : compatible with TextAE and PubAnnotation</li> <li>-g : generic format (default) with the format - tweetID TAB termID TAB startSpan TAB endSpan. </li> <li>-c - format compatible with Colab notebook </li></ul> | No. Default is set to generic |


How to run the dictionary based annotator:
```
python SMMT_NER_basic.py -i TSV_source_file.tsv -d dictionary_file.csv -o outputfile.ann -f b

python SMMT_NER_basic.py -i TSV_source_file.tsv -d dictionary_file.csv -o outputfile.json -f t

python SMMT_NER_basic.py -i TSV_source_file.tsv -d dictionary_file.csv -o outputfile.json -f c

python SMMT_NER_basic.py -i TSV_source_file.tsv -d dictionary_file.csv -o outputfile.json -f g


```