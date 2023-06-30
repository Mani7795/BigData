# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 12:16:46 2023

@author: mani
"""
from pymongo import MongoClient
import time

start_time = time.time()
client: MongoClient = MongoClient('127.0.0.1',27017)
db = client["Assigment1"]
tweets = db["10000 tweets"]
def mergeSort(tweets):
    if len(tweets)>1:    
        mid = len(tweets) // 2
        lower_half = tweets[:mid]
        upper_half = tweets[mid:]        
        lower_half = mergeSort(lower_half)
        upper_half = mergeSort(upper_half)        
        return merge(lower_half, upper_half)
    else:
        return tweets
def merge(lower_half, upper_half):
    tweetSorted = []
    i=j=0    
    while i<len(lower_half) and j<len(upper_half):
        if lower_half[i]['id_str'] < upper_half[j]['id_str']:
            tweetSorted.append(lower_half[i])
            i += 1
        else:
            tweetSorted.append(upper_half[j])
            j += 1    
    tweetSorted += lower_half[i:]
    tweetSorted += upper_half[j:]    
    return tweetSorted



doc = tuple(tweets.find())
tweets = mergeSort(doc)

with open('sortedIds.txt', 'w') as f:
    for tweet in tweets:
        f.write(tweet['id_str']+ "\n")
end_time = time.time()
print(end_time - start_time)