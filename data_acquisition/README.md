# Social Media Mining Toolkit - Data Annotation and Standardization Tools

## NOTE: For all tools in this folder you need to have Twitter Authentication Keys

## Utilities available:

**search_generic.py** This utility allows you to pass a few query terms and the tool with go to the Twitter stream and collect available tweets using the set of keywords. If you select a rare keyword this might end very shortly. However, if you select a very generic keyword, this utility will continue to loop gathering tweets until closed manually. The purpose of this is to leave the tool running on a separate process and constantly collect tweets for a period of time.

### Output: 
Series of json files with the keyword you searched as a prefix.


IMPORTAT: This tool needs your keys to be placed on a file called auth.py. We provide a template called copy_auth.py that you need to fill in with your API keys and rename to auth.py.

## Scraping Tool:

**scrape.py** This utility allows users to pass a list of Twitter userNames/handles, a starting date, and an ending date for scraping. You can pass these parameters on the _userConfig.py_ file. You can pass one or many users, making sure each one has a corresponding start and end date. The file is structured as a Python list were you edit the individual elements. The provided _userConfig.py_ file is an example of how to gather the Tweets of Donald Trump for a give particular date. The intended purpose of this tool is to gather historical tweets in order for a time range that are otherwise not available via the Twitter API. 

NOTE: You need to have your Twitter API keys on a file named: api_keys.json. We provide a template under copy_api_keys.sample, you should edit the file with the proper keys, save it, and rename it to api_keys.json. 

### Output:
A single file called tweetsids.json that contains the tweet identifiers for all the scrapped tweets. Note that you still need to 'hydrate' these identifiers to get the full proper json object. This file can either be hydrated with Twarc or use the get_metadata.py utility for this purpose.

**get_metadata.py** This utility will take the tweetsids.json file and hydrate all those tweets.

### Output: 
You will get three oput files: 

1. a tweets_ful.json file which contains the full json object for each of the hydrated tweets
1. a tweets_full.CSV file which contains partial fields extracted from the tweets._
1. a tweets_full.zip file which contains a zipped version of the tweets_full.json file.
1. a tweets_full_short.json which contains a shortened version of the hydrated tweets. 

