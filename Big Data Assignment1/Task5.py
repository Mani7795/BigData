# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 10:17:47 2023

@author: mani
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from dask import dataframe as d
#Taking output which we got from Task1 (Body.txt)
with open('body.txt', 'r', encoding="utf8") as file:    
    keyword = file.read()
#Storing keyword in list
keyword = [keyword]

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(keyword)
#print(X)
#Taking 1 row of vectorizer and converting it into dataframe and arranging them in ascending order based on TF_IDF column
freq = pd.DataFrame(X[0].T.toarray() , index=vectorizer.get_feature_names_out(),columns=["tfidf"])
#df = df.rename(columns={None: 'Keywords'})
#print(df)
result = freq.sort_values("tfidf",ascending=False)
#print(result)
result.to_csv('vectorMatrix.csv', index=True)
#Taking that output(result) from data frame and storing it in vectorMatrix CSV 
value=d.read_csv('vectorMatrix.csv', sep = ',', header = 0)
result=value.compute()           #Using dask to compute the result and parallely run each vector
N=int(input("Enter the top N of keywords with highest Frequency: "))
print(result.head(N))