# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 22:38:41 2023

@author: mani
"""
from pymongo import MongoClient

from mrjob.job import MRJob
from Task1 import extractKeyword


client: MongoClient = MongoClient('127.0.0.1',27017)
db = client["Assigment1"]
tweets = db["10000 tweets"]
tweetText = []

for text in tweets.find():
    tweet_body = text['text']
    tweet_body = extractKeyword(tweet_body)
    tweetText.append(tweet_body)
  
with open('body.txt', 'w', encoding='utf-8') as f:
    for tweet_body in tweetText:
        f.write(str(tweet_body))
        f.write('\n')
        
#WORD_REGEX = re.compile(r"[\w]+")
#Remove_link = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
class WordCount(MRJob):
    def mapper(self, _, line):
        keywords = extractKeyword(line)
        for k in keywords:
            yield k.lower(), 1
    def reducer(self, word, counts):
        yield word, sum(counts)
if __name__ == "__main__":
    WordCount.run()