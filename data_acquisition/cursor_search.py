#%%
import tweepy
import time
from copy_auth import TwitterAuth
import json


auth = tweepy.OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)

api = tweepy.API(auth_handler=auth, parser=tweepy.parsers.JSONParser())

def limithandler(cursor):
    while True:
        try:
            yield next(cursor)
        except tweepy.RateLimitError:
            time.sleep(60)

#%%
terms='cpac2021 trump2024 maga2024'
for term in terms.split(' '):
    cursor = tweepy.Cursor(api.search_30_day, query=term, maxResults=100, 
                            fromDate='202102250000', toDate='202102282359', 
                            environment_name=TwitterAuth.environment_label).pages(2)
    with open(f'{term}.json', 'w') as datafile:
        pages = []
        for page in limithandler(cursor):
            pages.append(page)
        datafile.write(json.dumps(pages))
# %%
with open('trump2024.json') as jf:
    s = jf.read()
    data = json.loads(s)
# %%
