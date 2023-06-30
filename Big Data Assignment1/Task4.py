# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 23:17:33 2023

@author: mani
"""

from mrjob.job import MRJob
import re 
from pymongo import MongoClient

import time

client: MongoClient = MongoClient('127.0.0.1',27017)
db = client["Assigment1"]
tweets = db["10000 tweets"]
id_text = []

WORD_RE = re.compile(r"\w+")

for ids in tweets.find():
    id_str = ids['id_str']
    id_text.append(id_str)

with open('ids.txt', 'w', encoding='utf-8') as f:
    for id_str in id_text:
        f.write((id_str))
        f.write('\n')

class sortIds(MRJob):
    def mapper(self, _, line):
        ids = line 
        ids_int = int(ids)
        yield ids_int, line
    def reducer(self, ids_int, lines):
        sort_ids = sorted(lines)
        for ids in sort_ids:
            yield None, ids 
start_time = time.time()            
if __name__ == "__main__":
    
    sortIds.run()
end_time = time.time()
print(end_time - start_time)