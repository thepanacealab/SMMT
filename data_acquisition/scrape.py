# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 21:22:50 2019

@author: KhanC
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep
#from xvfbwrapper import Xvfb
#from pyvirtualdisplay import Display
from selenium.webdriver.firefox.options import Options

import json
import datetime
import userConfig


# edit user list
users = userConfig.user_list
userssD = userConfig.user_sDate
userseD = userConfig.user_eDate

# only edit these if you're having problems
delay = 1  # time to wait on each page load before reading the page

#options = Options()
#options.headless = True
#options.add_argument("--headless")

driver = webdriver.Firefox()   #Safari()  # options are Chrome() Firefox() Safari()

twitter_idsF = 'test_tids.json'
twitter_ids_filename = 'tweetids.json'
ids = []

def format_day(date):
    day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
    month = '0' + str(date.month) if len(str(date.month)) == 1 else str(date.month)
    year = str(date.year)
    return '-'.join([year, month, day])

def form_url(user, since, until):
    p1 = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3A'
    p2 =  user + '%20since%3A' + since + '%20until%3A' + until + 'include%3Aretweets&src=typd'
    return p1 + p2

def increment_day(date, i):
    return date + datetime.timedelta(days=i)

options = Options()
options.headless = True
#options.add_argument("--headless")
#display = Display(visible=0, size=(800, 600))
#display.start()

#vdisplay = Xvfb()
#vdisplay.start()

uCnt=0
for user in users:
    sYear, sMonth, sDay = userssD[uCnt].split('-')
    eYear, eMonth, eDay = userseD[uCnt].split('-')
    start = datetime.datetime(int(sYear), int(sMonth), int(sDay))  # year, month, day
    end = datetime.datetime(int(eYear), int(eMonth), int(eDay))  # year, month, day
    
    days = (end - start).days + 1
    id_selector = '.time a.tweet-timestamp'
    tweet_selector = 'li.js-stream-item'
    user = user.lower()
    
    for day in range(days):
        d1 = format_day(increment_day(start, 0))
        d2 = format_day(increment_day(start, 1))
        url = form_url(user, d1, d2)
        print(url)
        print(d1)
        driver.get(url)
        sleep(delay)
    
        try:
            found_tweets = driver.find_elements_by_css_selector(tweet_selector)
            increment = 10
    
            while len(found_tweets) >= increment:
                print('scrolling down to load more tweets')
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(delay)
                found_tweets = driver.find_elements_by_css_selector(tweet_selector)
                increment += 10
    
            print('{} tweets found, {} total'.format(len(found_tweets), len(ids)))
    
            for tweet in found_tweets:
                try:
                    id = tweet.find_element_by_css_selector(id_selector).get_attribute('href').split('/')[-1]
                    ids.append(id)
                except StaleElementReferenceException as e:
                    print('lost element reference', tweet)
    
        except NoSuchElementException:
            print('no tweets on this day')
    
        start = increment_day(start, 1)
    uCnt=uCnt+1
all_ids = ids
data_to_write = list(set(all_ids))
print('tweets found on this scrape: ', len(ids))
print('total tweet count: ', len(data_to_write))

with open(twitter_ids_filename, 'w') as outfile:
    json.dump(data_to_write, outfile)

print('all done here')
#vdisplay.stop()
#display.stop()
driver.close()
