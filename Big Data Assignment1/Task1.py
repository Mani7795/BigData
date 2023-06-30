# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 11:51:15 2023

@author: mani
"""

from pymongo import MongoClient
import re
import nltk
from gensim import corpora, models
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from rake_nltk import Rake
from nltk.stem import PorterStemmer 
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

rake_nltk_var = Rake()

client: MongoClient = MongoClient('127.0.0.1',27017)
db = client["Assigment1"]
tweets = db["10000 tweets"]


def remove_stopwords(words): 
    """returns list of words without inconsequetial/unimportant/common words""" 
    result= [] 
    for w in words: 
        if w not in stopwords.words("english"): 
            result.append(w) 
    return result 

def stem_words(words): 
    """reduces words to their root word by removing derivational affixes""" 
    ps: PorterStemmer = PorterStemmer() 
    result= [] 
    for w in words: 
        result.append(ps.stem(w)) 
    return result 

def extractKeyword(text): 
    text = re.sub(r"[^\w]"," ",text) #removes non-alphabetical symbols (like punctuation and numbers)
#    text = re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', ' ', text)
    text = re.sub(r'http\S+|www\S+',' ', text)   #removing links
    
    words= word_tokenize(text) #convert into list of words 
    words = remove_stopwords(words) #remove stopwords 
    words = stem_words(words) #make the words undergo a form of linguistic normalisation 
    tokens = nltk.word_tokenize(text)
    keywords= nltk.pos_tag(tokens)#run Parts-of-Speech tagging to identify grammatical groupings of keywords 
    return keywords

def csvFormat(keywords): 
    """takes in a list of keyword-POS pairings and converts to CSV format"""
    keywords_csv = ','.join(keywords)
    
    return keywords_csv 

def filterText(text):
    text = re.sub(r'http\S+|www\S+',' ', text)
    text = re.sub(r"[^\w]"," ", text)   #removes non-alphabetical symbols (like punctuation and numbers)    
    return text

#EXTRACTING KEYWORDS FROM THE TEXT FIELD IN TWEETS
for t in tweets.find({},{"user":1,"text":1,"id_str":1}):   
    text = t['text'] 
    text = filterText(text)                             #filterText function is user-defined function used for removing unwanted spaces and links from the text
    rake_nltk_var.extract_keywords_from_text(text)      #extract_keywords from text is pre-defined function taken from rake-nltk-var package
    keywords = rake_nltk_var.get_ranked_phrases()
    keyword=csvFormat(keywords)              #keywords are converted into CSV format
    #Using update query based on user id each keywords are updated in database with new key/value pair
    tweets.update_many({                        
        "user.id":t["user"]["id"]},
        {"$set":{"keywords":keyword}})
    #print(csv)
    #for k in keywords:
     #   print(k)

 
filterPOS = ['NN', 'NNS', 'NNP', 'NNPS']    #Part of Speech list that we need to extract
for t in tweets.find({},{"user":1,
                         "text":1,
                         "id_str":1}):
    text = t['text']                        #Each tweets text is stored in text variable
    text = extractKeyword(text)      #Extracting keyword using the defined Function
    part_tags = [
        (word, pos) for word, pos in text
        if pos in filterPOS]
    entity_keyword = [word for word, pos in part_tags] 
    tweets.update_many({
        "user.id" : t["user"]["id"]},
        {"$set" : {"entity_keyword": entity_keyword}})


#EXTRACTING TOPIC OF THE TWEET 

for t in tweets.find({},{"user":1,"text":1,"_id":1}):
    text = t['text']
    words = [word for word in simple_preprocess(text) if word not in stopwords.words("english")]    #Tokenize and Lower case all the words and removing stopwords from the Text
    if not words:
        continue
    dictionary = corpora.Dictionary([words])        #Each words get their own Word_id which are taken from dictionary
    corpus = [dictionary.doc2bow(doc) for doc in [words]]
# Build LDA model
    lda_model = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=1)
# Print topics
    topics = lda_model.get_topic_terms(topicid=0, topn=10)  
    for word, p in topics:
        tweets.update_many({
            "user.id": t["user"]["id"]},
            {"$set": {"topic":(f"{dictionary[word]}:{p}")}})

sid = SentimentIntensityAnalyzer()
for t in tweets.find({},{"user":1,"text":1,"id_str":1}):
    text = t['text']
    scores = sid.polarity_scores(text)
    tweets.update_many({
        "user.id":t["user"]["id"]},
        {"$set":{"sentiment": scores}})




