# -*- coding: utf-8 -*-
"""
Created on Mon May  8 16:02:36 2023

@author: mani

"""

import time
points = []

n= 0
with open("150K Data Points for R-Tree Construction.txt", 'r') as dataset:
    for data in dataset.readlines():                                        #spliting the data points file to id, x and y
        data = data.split()
        points.append({
            'id': int(data[0]),
            'x': int(data[1]),
            'y': int(data[2])
            })
        n+=1
        
queries = []

i = 0
with open("200 Range Queries.txt", 'r') as datapoints:
    for query in datapoints.readlines():
        query = query.split()                                       #splitting the query file to id,x1,x2,y1,y2
        queries.append({
            'id': int(query[0]),
            'x_1': int(query[1]),
            'x_2': int(query[2]),
            'y_1': int(query[3]),
            'y_2': int(query[4])
            })
start_time = time.time()
n=1        
for query in queries:
    count = 0    
    for point in points:
        if query['x_1']<= point['x']<= query['x_2'] and query['y_1']<=point['y'] <= query['y_2']:           #This line is checking if the point lie in query range or not
            count+=1
    
    print("Query",+n," = ", +count, end = " ")
    n = n+1
end_time = time.time()
exe_time = end_time - start_time
print("The query processing Time for Sequential Scan is: ", +exe_time)              #Time taken for executing the sequential based sacn search
print("The average query time for each is: ", exe_time/200)