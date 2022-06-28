# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 11:46:55 2021

@author: mahon
"""

###MERGE DATA

import pandas as pd
from bs4 import BeautifulSoup
import time
import re
import nltk 
import string
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import requests

#%%
excluded_words=pd.read_csv(r"C:\Users\mahon\Documents\Python Scripts\Excluded_Words.csv")
excluded_words=excluded_words.values.tolist()

excluded_bigrams=pd.read_csv(r"C:\Users\mahon\Documents\Python Scripts\Excluded_Bigrams.csv")
excluded_bigrams=excluded_bigrams.values.tolist()

excluded_trigrams=pd.read_csv(r"C:\Users\mahon\Documents\Python Scripts\Excluded_Trigrams.csv")
excluded_trigrams=excluded_trigrams.values.tolist()

for i in range(len(excluded_bigrams)):
    excluded_bigrams[i] = excluded_bigrams[i][0]

for i in range(len(excluded_trigrams)):
    excluded_trigrams[i] = excluded_trigrams[i][0]
    
for i in range(len(excluded_words)):
    excluded_words[i] = excluded_words[i][0]


#%%
FN_Tweets=pd.read_csv(r"C:\Users\mahon\Documents\Python Scripts\FN_Tweets.csv")

FN_Tweet_concat=pd.DataFrame()


N=len(FN_Tweets['text'])

FN_Tweets['Date']=''
date=list(FN_Tweets['created_at'])
for j in range(N):
    date[j]=date[j][0:7]    
    FN_Tweets['Date'][j]=date[j]

date_range=set(list(FN_Tweets['Date']))
date_range = list(date_range)

separator = ', '

K=len(date_range)

lst0=["Fox Twitter"]


for i in range(K):
    print(i)
    indx=FN_Tweets.index[FN_Tweets['Date'] == date_range[i]].tolist()
    texts=FN_Tweets['text'][indx]
    texts=texts.tolist()
    txt=separator.join(texts)
    
    URLless_string = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', txt)
    
    lst1=[date_range[i]]
    lst2=[URLless_string]
    FNTweet_df_temp=pd.DataFrame({'Speaker':lst0, 'Date': lst1,'Text': lst2})
    
    FN_Tweet_concat=pd.concat([FN_Tweet_concat,FNTweet_df_temp])   
    
FN_Tweet_concat.to_csv("concat.csv") 
FN_Tweets=pd.read_csv(r"C:\Users\mahon\concat.csv")
N=len(FN_Tweets['Text'])

import random
size=100
#randy=[random.randint(0, N) for iter in range(size)]
#rand_list=randy
rand_list=random.sample(range(N), size)

texts = ["" for i in range(N)]

j=0

import random
size=100
rand_list=random.sample(range(N), size)

texts = ["" for i in range(N)]
FN_tweet_words_df=pd.DataFrame()
FN_tweet_bigrams_df=pd.DataFrame()
FN_tweet_trigrams_df=pd.DataFrame()

    
for j in range(N):
    
    print(j)
    
    texts=FN_Tweets['Text'][j]
    date=FN_Tweets['Date'][j][:7]

    texts=texts[:texts.find('http')]

    tokens=nltk.tokenize.RegexpTokenizer("[\\w']+|[^\\w\\s]+").tokenize(texts)
    tokens=list(filter(lambda w: not w in stops,tokens))
    tokens = list(filter(lambda token: token not in string.punctuation, tokens))
    tokens = list(filter(lambda token: token not in excluded_words, tokens))

    bigram = list(ngrams(tokens, 2)) 
    for i in range(len(bigram)):
        bigram[i]=str(bigram[i])

    bigram=list(filter(lambda w: not w in excluded_bigrams,bigram))
    
    trigram=list(ngrams(tokens,3))
    for i in range(len(trigram)):
        trigram[i]=str(trigram[i])

    trigram=list(filter(lambda w: not w in excluded_trigrams,trigram))


    size_token=len(tokens)
    size_bigram=len(bigram)
    size_trigram=len(trigram) 

 #Generate Words DF
    ID=FN_Tweets['Speaker'][j]
    lst1=[ID]*size_token
    
    lst3=[date]*size_token
    
    
    words_df_temp=pd.DataFrame({'Speaker': lst1,'Date':lst3,'Word': tokens})
    
    
    #Generate Bigrams DF
    ID=FN_Tweets['Speaker'][j]
    lst1=[ID] * size_bigram
    
    lst3=[date]*size_bigram
    
    bigrams_df_temp=pd.DataFrame({'Speaker': lst1,'Date':lst3,'Phrase': bigram})
    
    
    #Generate Trigrams DF
    ID=FN_Tweets['Speaker'][j]
    lst1=[ID] * size_trigram
    
    
    lst3=[date] * size_trigram
    
    trigrams_df_temp=pd.DataFrame({'Speaker': lst1,'Date':lst3,'Phrase': trigram})
    
    FN_tweet_words_df = pd.concat([FN_tweet_words_df,words_df_temp])
    FN_tweet_bigrams_df = pd.concat([FN_tweet_bigrams_df,bigrams_df_temp])
    FN_tweet_trigrams_df = pd.concat([FN_tweet_trigrams_df,trigrams_df_temp])



FNTW_words=pd.concat([FN_tweet_words_df,fox_words_df])
FNTW_bigrams=pd.concat([FN_tweet_bigrams_df,fox_bigrams_df])
FNTW_trigrams=pd.concat([FN_tweet_trigrams_df,fox_trigrams_df])