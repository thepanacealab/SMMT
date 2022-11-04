# Social Media Mining Toolkit - Data Acquisition Tools

## NOTE: For all tools in this folder, you need to have Twitter Authentication Keys

## Utilities available:

**search_generic.py** This utility allows you to pass a few query terms and the tool with go to the Twitter stream and collect available tweets using the set of keywords. If you select a rare keyword this might end very shortly. The purpose of this utility is to obtain "n" number of tweets. Please be careful with the "n". Please follow twitter download rates. If you exceed, twitter might block your keys.

**IMPORTANT**: This utility retrieves duplicate tweets if there are no new tweets in the search criteria. In order to obtain only unique tweets, set -d = n. Please see the usage for an example

|Arguments|Description|Required |
| ------------- | ------------- | ------------- |
|s|search terms for the query ; separated by ",". Look at the usage for example|Yes |
|n|Number of tweets required|Yes |
|d|Allow duplicate tweets?|No; Default value set to "Y" |

```
Usage : 

python search_generic.py -s "donald trump,coronavirus" -n 100

python search_generic.py -s "covid19" -n 300 -d n

```

### Output: 
Json files with the keyword you searched as a prefix.

_IMPORTANT: This tool needs your keys to be placed on a file called auth.py. We provide a template called copy_auth.py that you need to fill in with your API keys and rename to auth.py._

## Scraping Tool (test):

**scrape.py** This utility allows users to pass a list of Twitter userNames/handles, a starting date, and an ending date for scraping. You can pass these parameters on the _userConfig.py_ file. You can pass one or many users, making sure each one has a corresponding start and end date. The file is structured as a Python list where you edit the individual elements. The provided _userConfig.py_ file is an example of how to gather the Tweets of Donald Trump for a give particular date. The intended purpose of this tool is to gather historical tweets in order for a time range that are otherwise not available via the Twitter API. 

_NOTE: You need to have your Twitter API keys on a file named: api_keys.json. We provide a template under copy_api_keys.sample, you should edit the file with the proper keys, save it, and rename it to api_keys.json._

### Output:
A single file called tweetsids.json that contains the tweet identifiers for all the scrapped tweets. Note that you still need to 'hydrate' these identifiers to get the full proper json object. This file can either be hydrated with Twarc or use the get_metadata.py utility for this purpose.

**get_metadata.py** This utility will take a file which meets the following requirements:

1. a text file which contains one tweet id per line
1. a csv file which either contains one tweet id per line or contains at least one column of tweet ids
1. a tsv file which either contains one tweet id per line or contains at least one column of tweet ids


|Arguments|Description|Details|Required |
| ------------- | ------------- |------------- | ------------- |
|i|input text file name|A text file having one tweet id per line|Yes |
|o|output file name|4 output files will be created using the given output file name|Yes |
|k|Key file name|A json file which consists of details of the keys|Yes |
|c|id column name|the column name which contains tweet ids|No |
|m|tweet collection mode| e for extended mode| No! Default is set to compatible mode|


```
Usage : python get_metadata.py -i tweetids.txt -o hydrated_tweets -k api_keys.json
```

### Output: 
You will get four output files: 

1. a hydrated_tweets.json file which contains the full json object for each of the hydrated tweets
1. a hydrated_tweets.CSV file which contains partial fields extracted from the tweets.
1. a hydrated_tweets.zip file which contains a zipped version of the tweets_full.json file.
1. a hydrated_tweets_short.json which contains a shortened version of the hydrated tweets. 

**streaming.py** This utility fetches all the available tweets from the Twitter Stream. This utility does not take any search terms. Instead, it downloads tweets each day. The purpose of this is to leave the tool running on a separate process and constantly collect tweets for a period of time. The output of this utility is a json file with the 1% streaming sample with date of the day as the filename. This utility takes an argument to determine whether to compress the downloaded json file or not. If compression option is enabled, the json file is compressed in .zip format and file compression is carried out only after the day changes.
The compression wont work if the utility is terminated externally. 

**Note** - If you would like to compress the json file, you will have to send "compress" in the argument.

```
Usage 
python streaming.py nocompress #does not compress the json file
python streaming.py compress #compresses the json file


```
### Output: 
You will get one json file per day with the date as prefix of the file.  
