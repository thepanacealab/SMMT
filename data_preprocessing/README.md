# Social Media Mining Toolkit - Data Preprocessing Tools

## Utilities available:

### Separating tweets from an existing file via dictionary keywords

**separate_tweet_tsv.py** This utility will separate all tweets in TSV format that contain any of the terms in the given dictionary. It input for this utility is a TSV file with the format UserID TAB TweetID TAB TweetText TAB Date. The output of this utility is a tsv file with the same format as the input file.

Arguments: 

-d dictionary file
-i source file of tweets
-o output file of tweets

How to run the dictionary based separator:
```
python separate_tweet_tsv.py -i TSV_source_file.tsv -d dictionary_file.csv -o outputfile.tsv
```

**separate_tweets.py** This utility separates Tweet json objects from a file of twitter json objects (obtained by hydrating tweets) using a dictionary. The input for this utility is a json file with one json object per line. This program extracts the tweet text from the json object and uses the dictionary to identify the presence of dictionary. If there is a match, the tweet object is written to the output file. The output file consists of all such separated Tweet Json objects.

| Arguments     | Description | Required |
| ------------- | ------------- | ------------- |
| i  | input text file name   |   | Yes
| o  | output file name  |  | Yes |
| d | dictionary file name | Yes |
| t | no of threads (default is set to 1) | No |
| v | verbose – which gives all details of the program – total no of tweets processed, no of tweets separated, counts for each term saved in a csv file, total time taken to run the program | No |
| l | language | default set to English, but can take other languages “en” , “es”. | No |

How to run separate_tweets.py for obtaining Spanish tweets:
```
python separate_tweets.py -i inputfile.json -d dictionary_file.tsv -o outputfile.tsv -l es -v y
```

### Parsing Tweet JSON files

We provide two different json parsers:

**parse_json_lite.py** If your json file is less than 1GB (and you have enough RAM), this will be the one to use. It reads the full file in memory, so it should not be used for very large files.

**parse_json_heavy.py** This is intended for json files over 1GB and into the terabytes, which have 1 tweet per line. This reads the file line by line, using less memory.

NOTE: By default both parsers will output tab delimited files.

How to run the parsers:
```
python parse_json_lite.py FILENAME.json
```

or
```
python parse_json_heavy.py FILENAME.json
```

#### What fields do you want to extrat from your Tweet json? 

This depends on your application. By default both parsers will extract all fields. But you can limit to the only ones you want by editing the fields.py file and only leaving the ones you want.

Here is a list of available fields. Do not assume that all of your tweets will have all these elements, so don't be alarmed if they have null or empty values in them.

The official Tweet Data Directory can be found here: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object

```
fields =[
	'created_at', 
	'id', 
	'id_str', 
	'text', 
	'truncated', 
	'source', 
	'in_reply_to_status_id', 
	'in_reply_to_status_id_str', 
	'in_reply_to_user_id', 
	'in_reply_to_user_id_str', 
	'in_reply_to_screen_name', 
	'geo', 
	'coordinates', 
	'place', 
	'contributors', 
	'is_quote_status', 
	'retweet_count', 
	'favorite_count', 
	'favorited', 
	'retweeted', 
	'lang', 
	'entities.hashtags', 
	'entities.symbols', 
	'entities.user_mentions', 
	'entities.urls', 
	'user.id', 
	'user.id_str', 
	'user.name', 
	'user.screen_name', 
	'user.location', 
	'user.description', 
	'user.url', 
	'user.entities.description.urls', 
	'user.protected', 
	'user.followers_count', 
	'user.friends_count', 
	'user.listed_count', 
	'user.created_at', 
	'user.favourites_count', 
	'user.utc_offset', 
	'user.time_zone',
	'user.geo_enabled', 
	'user.verified', 
	'user.statuses_count', 
	'user.lang', 
	'user.contributors_enabled', 
	'user.is_translator', 
	'user.is_translation_enabled', 
	'user.profile_background_color', 
	'user.profile_background_image_url', 
	'user.profile_background_image_url_https', 
	'user.profile_background_tile', 
	'user.profile_image_url', 
	'user.profile_image_url_https', 
	'user.profile_banner_url', 'user.profile_link_color', 
	'user.profile_sidebar_border_color', 
	'user.profile_sidebar_fill_color',
	'user.profile_text_color',
	'user.profile_use_background_image',
	'user.has_extended_profile',
	'user.default_profile',
	'user.default_profile_image',
	'user.can_media_tag',
	'user.followed_by',
	'user.following',
	'user.follow_request_sent',
	'user.notifications',
	'user.translator_type',
	'user.entities.url.urls',
	'possibly_sensitive',
	'entities.media',
	'extended_entities.media',
	'place.id',
	'place.url',
	'place.place_type',
	'place.name',
	'place.full_name',
	'place.country_code',
	'place.country',
	'place.contained_within',
	'place.bounding_box.type',
	'place.bounding_box.coordinates',
	'quoted_status_id',
	'quoted_status_id_str',
	'quoted_status.created_at',
	'quoted_status.id',
	'quoted_status.id_str',
	'quoted_status.text',
	'quoted_status.truncated',
	'quoted_status.entities.hashtags',
	'quoted_status.entities.symbols',
	'quoted_status.entities.user_mentions',
	'quoted_status.entities.urls',
	'quoted_status.source',
	'quoted_status.in_reply_to_status_id',
	'quoted_status.in_reply_to_status_id_str',
	'quoted_status.in_reply_to_user_id',
	'quoted_status.in_reply_to_user_id_str',
	'quoted_status.in_reply_to_screen_name',
	'quoted_status.user.id',
	'quoted_status.user.id_str',
	'quoted_status.user.name',
	'quoted_status.user.screen_name',
	'quoted_status.user.location',
	'quoted_status.user.description',
	'quoted_status.user.url',
	'quoted_status.user.entities.url.urls',
	'quoted_status.user.entities.description.urls',
	'quoted_status.user.protected',
	'quoted_status.user.followers_count',
	'quoted_status.user.friends_count',
	'quoted_status.user.listed_count',
	'quoted_status.user.created_at',
	'quoted_status.user.favourites_count',
	'quoted_status.user.utc_offset',
	'quoted_status.user.time_zone',
	'quoted_status.user.geo_enabled',
	'quoted_status.user.verified',
	'quoted_status.user.statuses_count',
	'quoted_status.user.lang',
	'quoted_status.user.contributors_enabled',
	'quoted_status.user.is_translator',
	'quoted_status.user.is_translation_enabled',
	'quoted_status.user.profile_background_color',
	'quoted_status.user.profile_background_image_url',
	'quoted_status.user.profile_background_image_url_https',
	'quoted_status.user.profile_background_tile',
	'quoted_status.user.profile_image_url',
	'quoted_status.user.profile_image_url_https',
	'quoted_status.user.profile_banner_url',
	'quoted_status.user.profile_link_color',
	'quoted_status.user.profile_sidebar_border_color',
	'quoted_status.user.profile_sidebar_fill_color',
	'quoted_status.user.profile_text_color',
	'quoted_status.user.profile_use_background_image',
	'quoted_status.user.has_extended_profile',
	'quoted_status.user.default_profile',
	'quoted_status.user.default_profile_image',
	'quoted_status.user.can_media_tag',
	'quoted_status.user.followed_by',
	'quoted_status.user.following',
	'quoted_status.user.follow_request_sent',
	'quoted_status.user.notifications',
	'quoted_status.user.translator_type',
	'quoted_status.geo',
	'quoted_status.coordinates',
	'quoted_status.place',
	'quoted_status.contributors',
	'quoted_status.is_quote_status',
	'quoted_status.retweet_count',
	'quoted_status.favorite_count',
	'quoted_status.favorited',
	'quoted_status.retweeted',
	'quoted_status.possibly_sensitive',
	'quoted_status.lang',
	'quoted_status.entities.media',
	'quoted_status.extended_entities.media',
	'quoted_status.place.id',
	'quoted_status.place.url',
	'quoted_status.place.place_type',
	'quoted_status.place.name',
	'quoted_status.place.full_name',
	'quoted_status.place.country_code',
	'quoted_status.place.country',
	'quoted_status.place.contained_within',
	'quoted_status.place.bounding_box.type',
	'quoted_status.place.bounding_box.coordinates',
	'geo.type',
	'geo.coordinates',
	'coordinates.type',
	'coordinates.coordinates',
	'quoted_status.quoted_status_id',
	'quoted_status.quoted_status_id_str']
```
