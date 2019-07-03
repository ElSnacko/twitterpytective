# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 17:36:04 2019

"""


from bs4 import BeautifulSoup
import datetime
import pandas as pd
import time
import numpy
from selenium import webdriver as driver

class twitterpytective:
    tweetlines = []
    datelines = []
    picturelines = []
    passblock= []
    timetracker = {}

    def urlconfig(self,hashtag,startdate,enddate):
        #startdate and enddate needs to be in this format '2017-11-30'
        frame='https://twitter.com/search?l=en&q=%22%23{0}%22%20since%3A{1}%20until%3A{2}&src=typd'.format(hashtag,startdate,enddate)
        return frame

    def browser(self,url):
        option = driver.ChromeOptions().add_argument("--incognito")
        browser = driver.Chrome(r'chromedriver_win32\chromedriver.exe', chrome_options=option)
        browser.get(url)
        browser.minimize_window()
        res = browser.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(res,'html.parser')
        return soup, browser


    def scroller(self,browser):
        SCROLL_PAUSE_TIME = 1
        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def soupcollector(self,soup, browser):
        #scroll to the bottom
        self.scroller(browser)
    #for max tweet collection per day
        max_tweets=75
        for times in set(self.datelines):
            self.timetracker[times]= self.datelines.count(times)
    #Gathering dates w/ bs4
        created_at = soup.find_all('a', {'class':'tweet-timestamp'})
        for date in created_at:
            try:
                if int(self.timetracker[date.get_text()])>max_tweets:
                    self.passblock.append(1)
                    print(date.get_text() + ' is at {} entries'.format(self.timetracker[date.get_text()]))
                else:
                    self.datelines.append(datetime.datetime.strptime(date.get_text(), '%d %b %Y'))
                    self.passblock.append(0)
            except KeyError:
                self.datelines.append(datetime.datetime.strptime(date.get_text(), '%d %b %Y'))
                self.passblock.append(0)
    #Gathering tweets w/ bs4
        for count,tweet in enumerate(soup.find_all('p', {'class':"tweet-text"})):
            tweetstring = ' '.join([line.strip() for line in tweet.get_text().splitlines()])
            if self.passblock[count]==0:
    #scrub when the tweet has a picture in it
                if tweetstring.find('pic.twitter.com/')!=-1:
                    self.tweetlines.append(tweetstring[:tweetstring.find('pic.twitter.com/')])
                    self.picturelines.append(1)
                else:
                    self.tweetlines.append(tweetstring)
                    self.picturelines.append(0)
        browser.quit()
        data= {'date':self.datelines,'tweet':self.tweetlines,'picture(Y/N)':self.picturelines}
        return data

    def csver(self,data,name):
        twitterdf = pd.DataFrame(data=data)
        twitterdf.to_csv(name,index=False)
        
call = twitterpytective()
soup,browser =call.browser(call.urlconfig('hashtag', '2017-11-30','2018-02-28'))
call.csver(call.soupcollector(soup,browser),'twitterdata.csv')