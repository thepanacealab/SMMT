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
    #id_selector = '.time a.tweet-timestamp'
    #tweet_selector = 'li.js-stream-item'
    #This Works
    #tweet_selector = 'div.css-1dbjc4n.r-my5ep6.r-qklmqi.r-1adg3ll'
    tweet_selector = 'div.css-1dbjc4n.r-1d09ksm.r-18u37iz.r-1wbh5a2'
    #Tweets with threads get skipped, so here we get them
    tweet_selector_thread = 'article.css-1dbjc4n.r-1loqt21.r-1udh08x.r-o7ynqc.r-1j63xyz'
    #-This Works
    #tweet_selector = 'article.css-1dbjc4n.r-1loqt21.r-1udh08x.r-o7ynqc.r-1j63xyz'
    #tweet_selector = 'div.css-1dbjc4n.r-18u37iz.r-thb0q2'
    #tweet_selector = 'Timeline: Search timeline'
    #tweet_selector = 'div.css-1dbjc4n r-1j3t67a'
    #id_selector = 'div.css-4rbku5 css-18t94o4 css-901oao.r-1re7ezh.r-1loqt21.r-1q142lx.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-3s2u2q.r-qvutc0'
    #id_selector='div.css-1dbjc4n.r-1d09ksm.r-18u37iz.r-1wbh5a2'
    #id_selector='div.css-1dbjc4n.r-1d09ksm.r-18u37iz.r-1wbh5a2'
    id_selector='a.css-4rbku5.css-18t94o4.css-901oao.r-1re7ezh.r-1loqt21.r-1q142lx.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-3s2u2q.r-qvutc0'
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
            tweetsNormal =len(found_tweets)
            try:
                found_tweets2 = driver.find_elements_by_css_selector(tweet_selector_thread)
                tweetsThread = len(found_tweets2)
            except NoSuchElementException:
                tweetsThread = 0
            #print("Total tweets found: " + str(tweetsNormal + tweetsThread))

            increment = 10
    
            while len(found_tweets) >= increment:
                print('scrolling down to load more tweets')
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(delay)
                found_tweets = driver.find_elements_by_css_selector(tweet_selector)
                increment += 10
                tweetsNormal = len(found_tweets)
                try:
                    found_tweets2 = driver.find_elements_by_css_selector(tweet_selector_thread)
                    tweetsThread = len(found_tweets2)
                except NoSuchElementException:
                    tweetsThread = 0
            print("Total tweets found: " + str(tweetsNormal + tweetsThread))
            #print('{} tweets found, {} total'.format(len(found_tweets), len(ids)))
            #print("Selector found " + str(len(found_tweets)) + " tweets")
            for tweet in found_tweets: 
                #print(tweet.find_element_by_css_selector(id_selector))
                #print(tweet.find_element_by_css_selector(id_selector).get_attribute('href'))
                try:
                    id = tweet.find_element_by_css_selector(id_selector).get_attribute('href').split('/')[-1]
                    ids.append(id)
                except StaleElementReferenceException as e:
                    print('lost element reference', tweet)
            for tweet in found_tweets2:
                #print(tweet.find_element_by_css_selector(id_selector))
                #print(tweet.find_element_by_css_selector(id_selector).get_attribute('href'))
                try:
                    id = tweet.find_element_by_css_selector(id_selector).get_attribute('href').split('/')[-1]
                    ids.append(id)
                except StaleElementReferenceException as e:
                    print('lost element reference', tweet)
            print('{} tweets found, {} total'.format(len(found_tweets), len(ids)))

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
