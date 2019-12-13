"""
Author:AMJADHKHAN CA
Date: 13/12/2019
Purpose:Program for Scraping tweets from twitter based on the hash tags using twitter api
Modules used: tweepy,csv,pandas,json
"""

import tweepy
import csv
import pandas as pd
import json

with open('twitter_credentials.json') as cred_data:
	info = json.load(cred_data)
	consumer_key = info['CONSUMER_KEY']
	consumer_secret = info['CONSUMER_SECRET']
	access_key = info['ACCESS_KEY']
	access_secret = info['ACCESS_SECRET']


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

csvFile = open('ua.csv', 'a')
csvWriter = csv.writer(csvFile)
hashtag = input("Enter The hashtag you want to search : ") 

for tweet in tweepy.Cursor(api.search,q=hashtag,count=100,
                           lang="en",
                           since="2019-12-01").items():
    print (tweet.created_at, tweet.text)
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])


