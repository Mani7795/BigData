# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 10:30:27 2023

@author: mani
"""

from pymongo import MongoClient
import re
from mrjob.job import MRJob

client: MongoClient = MongoClient('127.0.0.1',27017)
db = client["Assigment1"]
tweets = db["10000 tweets"]
tweet_cities = []

for text in tweets.find():
    if 'location' in text['user']:
        tweet_city = text["user"]['location']['displayName']
        tweet_cities.append(tweet_city)
        
  
with open('cities.txt', 'w', encoding='utf-8') as f:
    for tweet_city in tweet_cities:
        f.write(str(tweet_city))
        f.write('\n')
        
#cities = []

#n = int(input('Enter number of cities: '))
#for i in range(0,n):
#    city = str(input())
#    cities.append(city)
#print(cities)
WORD_REGEX = re.compile(r"[\w]+")

cities = ['Sydney', 'Perth']
class cityCount(MRJob):
    def mapper(self, _, line):        
        for city in WORD_REGEX.findall(line):
            if city in cities:
                yield city.lower(), 1
    def reducer(self, city, counts):
        yield city, sum(counts)
        
if __name__ == "__main__":
    cityCount.run()
    