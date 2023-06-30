# -*- coding: utf-8 -*-
"""
Created on Mon May  8 16:02:36 2023

@author: mani

"""
import sys
import math
import time
points = []

n= 0
with open("150K Data Points for R-Tree Construction.txt", 'r') as dataset:
    for data in dataset.readlines():
        data = data.split()
        points.append({
            'id': int(data[0]),
            'x': int(data[1]),
            'y': int(data[2])
            })
#        print("id= ", (points[n]['id']), "x= ", (points[n]['x']), "y= ", points[n]['y'])
        n+=1
        
queries = []

i = 0
with open("200 Range Queries.txt", 'r') as datapoints:
    for query in datapoints.readlines():
        query = query.split()
        queries.append({
            'id': int(query[0]),
            'x_1': int(query[1]),
            'x_2': int(query[2]),
            'y_1': int(query[3]),
            'y_2': int(query[4])
            })
#        print(queries)
start_time = time.time()
n=1        
for query in queries:
    count = 0    
    for point in points:
        if query['x_1']<= point['x']<= query['x_2'] and query['y_1']<=point['y'] <= query['y_2']:
            count+=1
    
    print("Query",+n," = ", +count)
    n = n+1
end_time = time.time()
exe_time = end_time - start_time
print("The query processing Time for Sequential Scan is: ", +exe_time)