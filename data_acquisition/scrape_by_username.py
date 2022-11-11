from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import selenium.common.exceptions
import json, csv, datetime, time, re
import urllib.request, urllib.parse, urllib.error
import pandas as pd
import userConfig


def form_url(user, since, until):
    url = 'https://twitter.com/search?q=from%3A' + user + \
          '%20include%3Anativeretweets%20-filter%3Areplies%20since%3A'\
           + since+'%20until%3A' + until + '&src=typed_query'
    print("URL From a specific day: "+url)
    return url


def formatDate(time_str):
    date = time_str[0:10]
    time = time_str[11:19]
    utc_time_str = date + ' ' + time
    utc_time = datetime.datetime.strptime(utc_time_str,'%Y-%m-%d %H:%M:%S')
    utc_time = utc_time.strftime('%Y-%m-%d %H:%M:%S')
    return utc_time


def format_day(date):
    day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
    month = '0' + str(date.month) if len(str(date.month)) == 1 else str(date.month)
    year = str(date.year)
    return '-'.join([year, month, day])


def increment_day(date, i):
    return date + datetime.timedelta(days=i)


def countDown(minutes):
    if minutes > 1:
        print('\ntime out for %d mins...\n' % minutes)
    else:
        print('\ntime out for 1 min...\n')

    for min in range(minutes,-1,-1):
        if min == 0:
            print('\rGetting tweets...     ',flush=True)
            break
        for second in range(59, -1, -1):
            time.sleep(1)
            if second >= 10:
                print('time left %s:%s' % (min - 1, second), end='\r', flush=True)
            else:
                print('time left %s:0%s' % (min - 1, second), end='\r', flush=True)


def remove_duplicates(tweets_temp):
    unique_tweets = []
    seen = set()
    for tweet in tweets_temp:
        id = tweet['permalink']
        if id not in seen:
            seen.add(id)
            unique_tweets.append(tweet)
    return unique_tweets


def get_onepage_tweets(driver, tweets_selector, user):
    tweets = []
    try:
        tweets_elements = driver.find_elements(By.CSS_SELECTOR,tweets_selector)
        for element in tweets_elements:
            #print(element.get_attribute('innerHTML'))
            text = ''
            isRetweet = False
            isResponse = False
            hashtags = []
            mentions = []
            element_text = element.text
            #Sometimes tweet containers may be empty, therefore we must be sure there are no empty containers
            if element_text.strip() != "":
                try:
                    info_element = element.find_element(By.CSS_SELECTOR,'div:nth-child(1) > div > div > article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(3) > a')
                    permalink = info_element.get_attribute('href')
                    info = permalink.split('/')
                    # print(info)
                    user_name = info[-3]

                    if user_name.lower() != user.lower():
                        isRetweet = True

                    tweet_id = info[-1]
                    # print(user_name)
                except:
                    print('failed to fetch username and tweet id...')
                    continue

                try:
                    date_utc = element.find_element(By.CSS_SELECTOR,'div:nth-child(1) > div > div > article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(3) > a > time').get_attribute('datetime')
                    date = formatDate(date_utc)
                    # print(date)
                except:
                    date = None
                    print('failed to fetch date...')

                try:
                    no_elements_temp = len(element.find_elements(By.CSS_SELECTOR,'div:nth-child(1) > div > div > article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div'))
                    
                    if(no_elements_temp == 3):
                        retweets = element.find_element(By.CSS_SELECTOR,'div:nth-child(1) > div > div > article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(2) > div > div > div:nth-child(2) > span > span >span').get_attribute('innerHTML')
                        favorites = element.find_element(By.CSS_SELECTOR,'div:nth-child(1) > div > div > article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(3) > div > div > div:nth-child(2) > span > span >span').get_attribute('innerHTML')
                    if(no_elements_temp == 2):
                        retweets = element.find_element(By.CSS_SELECTOR,'div:nth-child(1) > div > div > article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div > div:nth-child(2) > div > div > div:nth-child(2) > span > span >span').get_attribute('innerHTML')
                        favorites = element.find_element(By.CSS_SELECTOR,'div:nth-child(1) > div > div > article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div > div:nth-child(3) > div > div > div:nth-child(2) > span > span >span').get_attribute('innerHTML')

                    # print(retweets,favorites)
                except:
                    retweets = favorites = None
                    print('failed to fetch retweets and favorites (may be zero)...')

                try:
                    to = element.find_element(By.CSS_SELECTOR,'div:nth-child(2) > div:nth-child(2) > div > div > div > div.css-1dbjc4n.r-9x6qib.r-1ylenci.r-rs99b7.r-1loqt21.r-dap0kf.r-1ny4l3l.r-1udh08x.r-o7ynqc.'
                                                            'r-6416eg > div > div.css-1dbjc4n.r-1awozwy.r-18u37iz.r-1wbh5a2.r-vlx1xi.r-156q2ks > div.css-1dbjc4n.r-1wbh5a2.r-1udh08x > div > div > div > div > di'
                                                            'v.css-1dbjc4n.r-18u37iz.r-1wbh5a2.r-1f6r7vd > div > span').text
                    to = re.sub('@','',to)

                    isResponse = True
                except:
                    to = ''

                try:
                    response_indicator = element.find_element(By.CSS_SELECTOR,
                        'div:nth-child(2) > div.css-1dbjc4n.r-4qtqp9.r-18u37iz.r-1wtj0ep.r-zl2h9q > div')

                    if response_indicator.text.startswith('Replying'):
                        isResponse = True
                        to_spans = response_indicator.find_element(By.CSS_SELECTOR,'span')

                        to_list = [to_spans[i].text.replace('@', '') for i in range(len(to_spans))]
                        to = ' '.join(to_list)
                except:
                    pass

                try:
                    text_element = element.find_element(By.CSS_SELECTOR,'div:nth-child(1) > div > div > article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)') 
                    contents = text_element.find_elements(By.XPATH,'span | a | div/span')

                    #no_content = 1
                    for content in contents:
                        #content_text = content.get_attribute('innerHTML')
                        content_text = content.text
                        #print("Number of content: "+str(no_content))
                        #print(str(content.text))
                        #no_content += 1
                        #print(content_text)

                        if content_text == '':
                            try:
                                # To convert emoji to text
                                emoji = content.find_element(By.CSS_SELECTOR,'div').get_attribute('aria-label')
                                emoji_utf = str(emoji.encode())
                                emoji_text = 'Emoji[' + emoji_utf + ']'

                                text += emoji_text if text == '' else ' '+emoji_text if text[-1] != ' ' else emoji_text
                            except NoSuchElementException:
                                pass
                        elif content_text.startswith('#'):
                            hashtags.append(content_text)
                            text += content_text if text == '' else ' ' + content_text if text[-1] != ' ' else content_text
                        elif content_text.startswith('@'):
                            mentions.append(content_text)
                            text += content_text if text == '' else ' ' + content_text if text[-1] != ' ' else content_text
                        
                        #elif content_text.startswith('<span aria-hidden="true" class="css-901oao css-16my406 r-poiln3 r-hiw28u r-qvk6io r-bcqeeo r-qvutc0">'):
                        #    link = re.sub('<span aria-hidden="true" class="css-901oao css-16my406 r-poiln3 r-hiw28u r-qvk6io r-bcqeeo r-qvutc0">','',content_text)
                        #    link = re.sub('</span>','',link)
                        #    text += ' ' + link.strip()
                        
                        elif content_text.startswith('http'):
                            text += ' '+content_text.strip()
                        else:
                            text += content_text.strip()
                        # puc = chr(0xE001)
                        # comment = comment.replace('\n',puc)
                    text = re.sub('\n',' ',text)
                    text = re.sub('\r','',text)
                    # print(comment)
                except:
                    print('error: ',permalink)
                    continue

                tweet_info = {'date': date,
                            'username': user_name,
                            'tweet_id': tweet_id,
                            'permalink': permalink,
                            'isRetweet': isRetweet,
                            'isResponse': isResponse,
                            'to': to,
                            'text': text,
                            'retweets': retweets,
                            'favorites': favorites,
                            'mentions': ' '.join(mentions),
                            'hashtags': ' '.join(hashtags)
                            }
                tweets.append(tweet_info)

    except NoSuchElementException:
        pass

    return tweets


def scrape_by_username(user_list, start_date, end_date):
    print('Getting tweets....')

    sYear, sMonth, sDay = start_date.split('-')
    eYear, eMonth, eDay = end_date.split('-')
    users = user_list

    final_tweets = []
    count = 0

    options = Options()
    options.headless = True
    driver_path = userConfig.driver_path
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # options.add_experimental_option("prefs",prefs)

    jsonfile_name = 'tweets_%s_%s_%s.json' % (user_list, start_date, end_date)
    tsvfile_name = 'tweets_%s_%s_%s.tsv' % (user_list, start_date, end_date)
    
    with open(tsvfile_name, 'w', newline='',encoding='utf-8') as outfile:
        fieldnames = ['date', 'username', 'tweet_id', 'permalink', 'isRetweet', 'isResponse', 'to', 'text', 'retweets', 'favorites',
                      'mentions', 'hashtags', 'geo']
        writer = csv.DictWriter(outfile, delimiter='\t', fieldnames=fieldnames)
        writer.writeheader()
        
        try:
            for user in users:
                
                start = datetime.datetime(int(sYear), int(sMonth), int(sDay))  # year, month, day
                end = datetime.datetime(int(eYear), int(eMonth), int(eDay))

                days = (end - start).days + 1

                for day in range(days):
                    d1 = format_day(increment_day(start, 0))
                    d2 = format_day(increment_day(start, 1))
                    print("============Checking tweets from day "+str(d1)+"================")
                    url = form_url(user, d1, d2)
                    driver = webdriver.Chrome(options=options, executable_path=driver_path)
                    # driver.implicitly_wait(5)
                    driver.get(url)
                    
                    time.sleep(3)
                     
                    tweets_selector = '#react-root > div > div > div:nth-child(2) > main > div > div > div > div > div > div:nth-child(3) > div > section > div > div > div[data-testid="cellInnerDiv"]'

                    last_height = 0
                    SCROLL_SIZE = 3000

                    oneday_tweets = []
                    
                    while True:
                        oneday_tweets += get_onepage_tweets(driver, tweets_selector, user)
                        
                        driver.execute_script("window.scrollBy(0, %s);" % SCROLL_SIZE)
                        time.sleep(2)

                        last_height += SCROLL_SIZE/2
                        new_height = driver.execute_script("return document.body.scrollHeight")

                        if last_height >= new_height:
                            oneday_tweets += get_onepage_tweets(driver, tweets_selector, user)
                            break

                    unique_tweets = remove_duplicates(oneday_tweets)

                    writer.writerows(unique_tweets)
                    outfile.flush()

                    final_tweets += unique_tweets
                    count += len(unique_tweets)

                    if count >= 3000:
                        countDown(3)
                        count = 0

                    start = increment_day(start,1)

                    driver.quit()

            df = pd.read_csv(tsvfile_name, sep='\t', encoding='utf-8')
            df.to_json(jsonfile_name, orient='records', indent=4)
            # with open(jsonfile_name, 'w', encoding='utf-8') as outfile:
            #     json.dump(final_tweets, outfile, indent=4, ensure_ascii=False)
            print('\n%i tweets are saved in %s' % (len(df),tsvfile_name))
            print('%i tweets are saved in %s' % (len(df), jsonfile_name))
        except:
            with open(jsonfile_name, 'w', encoding='utf-8') as outfile:
                json.dump(final_tweets, outfile, indent=4, ensure_ascii=False)
            print('\n%i tweets are saved in %s' % (len(final_tweets),tsvfile_name))
            print('%i tweets are saved in %s' % (len(final_tweets), jsonfile_name))
