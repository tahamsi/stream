# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 16:58:57 2023

@author: Taha Mansouri
"""

import tweepy
import socket
import preprocessor as p
import pandas as pd
import time

class TweetListener(tweepy.StreamingClient):
    
    def __init__(self, bearer, csocket):
        super(TweetListener, self).__init__(bearer)
        self.client_socket = csocket

    def on_tweet(self, tweet):
        if tweet.lang=="en" and tweet.referenced_tweets == None:
            clean_text = p.clean(tweet.text)
            print(clean_text)
            self.client_socket.send(clean_text.encode("utf-8"))
            time.sleep(5)
        return True
    
    def on_error(self, status_code):
        print(status_code)
        return True

def send_tweets(c_socket, search_terms,bearer):
    twitter_stream = TweetListener(bearer,c_socket)
    twitter_stream.add_rules(tweepy.StreamRule(search_terms))
    twitter_stream.filter(tweet_fields=["lang","referenced_tweets"], threaded=True)

def create_stream(search_terms,bearer,host='localhost', port=5555):
    new_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_skt.bind((host, port))
    print("Now listening on port: %s" % str(port))
    new_skt.listen(5)
    c , addr = new_skt.accept()
    print("Received request from: ", addr)
    send_tweets(c,search_terms,bearer)


def authenticate(api_key, api_secrets, access_token, access_secret):
    # Authenticate to Twitter V1.1
    auth = tweepy.OAuthHandler(api_key,api_secrets)
    auth.set_access_token(access_token,access_secret)
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print('Successful Authentication')
        return api, True
    except:
        print('Failed authentication')
        return api, False


def checkTweets(api,QueryTopic,lang='en',count=200):
    tweets = [tweet for tweet in tweepy.Cursor(api.search_tweets, q = QueryTopic, lang = lang, 
                                           result_type = "mixed", count = count).items(count)]
    to_extract = [
    'lang',
    'user',
    'created_at',
    'text',
    'retweeted',
    'favorited',
    'retweet_count',
    'favorite_count'
    ]
    tweet_entities = [('hashtags','text'), ('user_mentions','screen_name'), ('urls','expanded_url')]
    tweets_data = []
    for tweet in tweets:
        tweet = tweet._json
        tweet_data = {}
        for e in to_extract:
            try:
                tweet_data[e]=tweet[e]
            except:
                continue
        for entity in tweet_entities:
            entity_list = []
            for t in tweet['entities'][entity[0]]:
                entity_list.append(t[entity[1]])
            tweet_data[entity[0]] = entity_list
        tweets_data.append(tweet_data)

    df = pd.DataFrame(tweets_data)
    return df.to_json()

def getVibrationReadings(fileName, host='127.0.0.1', port=5556):
    ds = pd.read_csv(fileName)
    s = socket.socket()
    s.bind((host, port))
    print('socket is ready')
    s.listen(4)
    print('socket is listening')
    c_socket, addr = s.accept()
    print("Received request from: " + str(addr))
    count=0
    while count < len(ds):
        c_socket.send(ds.iloc[count]['Value'].to_json().encode("utf-8"))
        print(ds.iloc[count]['Value'].to_json().encode("utf-8"))
        count +=1
        time.sleep(5)
