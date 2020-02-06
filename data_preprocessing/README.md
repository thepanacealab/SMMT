## Social Media Mining Toolkit - Data Preprocessing Tools

# Utilities available:

** separate_tweet_tsv.py ** This utility will separate all tweets in TSV format that contain any of the terms in the given dictionary.

Arguments: 

-d dictionary file
-i source file of tweets
-o output file of tweets

How to run the dictionary based separator:
```
python separate_tweet_tsv.py -i TSV_source_file.tsv -d dictionary_file.csv -o outputfile.tsv
```
