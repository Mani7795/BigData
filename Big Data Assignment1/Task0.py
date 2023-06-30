# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 14:09:59 2023

@author: mani
"""

from pymongo import MongoClient


client: MongoClient = MongoClient('127.0.0.1',27017)
db = client["Assigment1"]
tweets = db["10000 tweets"]

for doc in tweets.find():
    updated_doc = {}
    value = doc['user']['id']
    value1 = str(value)
    value1 = value.split(':')
    ids = value1[-1]
    updated_doc['user.id'] = str(ids)
    tweets.update_many({"_id": doc["_id"]}, {"$set": updated_doc})
for doc in tweets.find():
    updated_doc = {}
    value = doc['id']
    value1 = str(value)
    value1 = value.split(':')
    ids = value1[-1]
    updated_doc['id'] = str(ids)
    tweets.update_many({"_id": doc["_id"]}, {"$set": updated_doc})
for tweet in tweets.find():
    tweet_id = tweet["_id"]
    id_str = tweet["id_str"]
    id_str = str(id_str)  # Convert the "id_str" field to an integer
    tweets.update_one({"_id": tweet_id}, {"$set": {"id_str": id_str}})
    
    
for doc in tweets.find():
    tweets.update_many({}, {
              "$rename":
                  {
                  "id":"id_str",
                  "user.displayName": "name",
                  "user.preferredUsername": "screenName",
                  "user.link": "user.url",
                  "user.summary": "user.description",
                  "actor": "user",
                  "body":"text",
                  "postedTime":"created_at",
                  "twitter_entities":"entities"                  
                  },
                  "$unset": 
                       {
                     "entities.media":"",
                     "entities.symbols":"",
                    "link":"",
                    "actor.links":"",
                    "actor.twitterTimeZone": "", 
                    "actor.followersCount": "", 
                    "actor.friendsCount":"", 
                    "actor.listedCount": "", 
                    "actor.friendsCount":"", 
                    "actor.statusesCount":"", 
                    "actor.verified":"",
                    "actor.utcOffset":"",
                    "actor.postedTime":"",
                    "actor.favoritesCount":"",
                    "actor.languages":"",
                    "actor.image":"",
                    "actor.objectType":"",
                    "actor.location.objectType":"",
                    "objectType":"",
                    "verb":"",
                    "generator":"",
                    "provider":"",
                    "object":"", 
                    "favoritesCount":"",
                    "twitter_filter_level":"",
                    "twitter_lang":"",
                    "retweetCount":"",
                    "gnip":"",
                    "twitter_extended_entities":""
              }
                       }
        )
            
            
            
           