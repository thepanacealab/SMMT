## Social Media Mining Toolkit - Data Annotation and Standardization Tools

# Utilities available:

**SMMT_NER_basic.py** This utility will annotate tweets in a given TSV file (TSV_source.tsv) with format tweetID tab Text, with a given dictionary dictionary_file.txt - with format termID TAB termString. The output will be saved in the give outputfile.tsv, with the format tweetID TAB termID TAB startSpan TAB endSpan.
 

Arguments: 

-d dictionary file
-i source file of tweets
-o output file of annotations

How to run the dictionary based separator:
```
python SMMT_NER_basic.py -i TSV_source_file.tsv -d dictionary_file.csv -o outputfile.tsv
```
