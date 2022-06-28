# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 14:47:09 2021

@author: mahon
"""

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
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error


#Import Exclusion lists -- required for all sections!
stops=set(stopwords.words('english'))

excluded_words=pd.read_csv(r"C:\Users\mahon\Documents\Python Scripts\Excluded_Words.csv")
excluded_words=excluded_words.values.tolist()

excluded_bigrams=pd.read_csv(r"C:\Users\mahon\Documents\Python Scripts\Excluded_Bigrams.csv")
excluded_bigrams=excluded_bigrams.values.tolist()

excluded_trigrams=pd.read_csv(r"C:\Users\mahon\Documents\Python Scripts\Excluded_Trigrams.csv")
excluded_trigrams=excluded_trigrams.values.tolist()

#Convert to iterable
for i in range(len(excluded_bigrams)):
    excluded_bigrams[i] = excluded_bigrams[i][0]

for i in range(len(excluded_trigrams)):
    excluded_trigrams[i] = excluded_trigrams[i][0]

for i in range(len(excluded_words)):
    excluded_words[i] = excluded_words[i][0]

numbers=range(1000)
numbers=list(numbers)
numbers=[format(x, '') for x in numbers]


#Extract URLS
data=pd.read_csv(r"C:\Users\mahon\Documents\Python Scripts\CNN_URLS_List.csv")
urls=data['URLS']
N=len(urls)

conn = sqlite3.connect(r'C:\Users\mahon\Documents\Python Scripts\pythonsqlite.db')
sql_create_bigrams_table = """ CREATE TABLE IF NOT EXISTS CNN_test (
                                        Speaker text,
                                        Date text ,
                                        Network text,
                                        Phrase text
                                    ); """

c = conn.cursor()
c.execute(sql_create_bigrams_table)


#Append URLs with correct address -- CNN Only
for i in range(N):
    urls[i]='http://transcripts.cnn.com/'+urls[i][7:]

#Initialize vectors and DFs
texts = ["" for i in range(N)]

CNN_words_df=pd.DataFrame()
CNN_bigrams_df=pd.DataFrame()
CNN_trigrams_df=pd.DataFrame()

import random
size=45000
rand_list=random.sample(range(N), size)

from urllib.error import HTTPError

its=0
N/100

for k in range(450):
    CNN_bigrams_df=pd.DataFrame()
    lower=100*k
    upper=100*(k+1)-1
    #WEBSCRAPE UTILITY
    for j in range(lower,upper):

        dt=data['Year'][j]+"-"+data['Month'][j]
        
        test=its/(size/100)
        if test.is_integer():
            print("Scraping CNN archieves. Progress:")
            print(str((its/size*100)))

        try:    
            page = urlopen(urls[j])
    

            html_bytes = page.read()
            html = html_bytes.decode("utf-8")
    
            soup = BeautifulSoup(html, "html.parser")
            texts[j]=soup.get_text()
            texts[j].replace('\n','')

            tokens=nltk.tokenize.RegexpTokenizer("[\\w']+|[^\\w\\s]+").tokenize(texts[j])
            tokens = list(filter(lambda token: token not in string.punctuation, tokens))
            filter(lambda x: x in printable, tokens)
            tokens = [sub.replace("ago", '') for sub in tokens]
            tokens = [sub.replace('+', '') for sub in tokens] 
            tokens = [sub.replace(',', '') for sub in tokens] 
            tokens = [sub.replace('`', '') for sub in tokens] 
            tokens = [sub.replace('-', '') for sub in tokens]
            tokens = [sub.replace("'", '') for sub in tokens]
            tokens = [sub.replace("’", '') for sub in tokens]
            tokens = [sub.replace("”", '') for sub in tokens]
            tokens = [sub.replace("”", '') for sub in tokens]
            tokens = [sub.replace("‘", '') for sub in tokens]
            tokens = [sub.replace("“", '') for sub in tokens]
            tokens = [sub.replace(")", '') for sub in tokens]
            tokens = [sub.replace("(", '') for sub in tokens]
            tokens = [sub.replace("]", '') for sub in tokens]
            tokens = [sub.replace("00", '') for sub in tokens]
            tokens = [sub.replace("000", '') for sub in tokens]
            tokens = [sub.replace("[", '') for sub in tokens]
            tokens = [sub.replace('."', '') for sub in tokens]
            tokens = [sub.replace('NewsFacebookTwitterFlipboardPrintEmailYou', '') for sub in tokens]
            tokens = [sub.replace('NewsFacebookTwitterFlipboardPrintEmailNow', '') for sub in tokens]
            tokens = [sub.replace('"', '') for sub in tokens]
            tokens = [sub.replace('Fox', '') for sub in tokens]
            tokens = [sub.replace('com', '') for sub in tokens] 
            tokens=list(filter(lambda a: not a in numbers,tokens))
            tokens=list(filter(lambda a: a != '', tokens))
            tokens=list(filter(lambda w: not w in stops,tokens))
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
    
            Net=data['Program'][j]
            lst2=[Net]*size_token
            lst3=[dt]*size_token
            lst4=['CNN']*size_token
    
    
            words_df_temp=pd.DataFrame({'Speaker': lst2,'Date':lst3,'Network':lst4,'Word': tokens})
    
    
        #Generate Bigrams DF
    
            Net=data['Program'][j]
            lst2=[Net]*size_bigram
            lst3=[dt]*size_bigram
            lst4=['CNN']*size_bigram
    
            bigrams_df_temp=pd.DataFrame({'Speaker': lst2,'Date':lst3,'Network':lst4,'Phrase': bigram})
    
        #Generate Trigrams DF
    
            Net=data['Program'][j]
            lst2=[Net]* size_trigram
            lst3=[dt] * size_trigram
            lst4=['CNN']*size_trigram
    
            trigrams_df_temp=pd.DataFrame({'Speaker': lst2,'Date':lst3,'Network':lst4,'Phrase': trigram})
    
        #Concat is slow as fuck -- there must be a better way!
            CNN_words_df = pd.concat([CNN_words_df,words_df_temp])
            CNN_bigrams_df = pd.concat([CNN_bigrams_df,bigrams_df_temp])
            #CNN_trigrams_df = pd.concat([CNN_trigrams_df,trigrams_df_temp])
            its=its+1
        
        except: HTTPError
    
    
    CNN_bigrams_df.to_sql('Master_bigrams', conn, if_exists='append', index=False)
    CNN_words_df.to_sql('Master_words', conn, if_exists='append', index=False)
    CNN_trigrams_df.to_sql('Master_trigrams', conn, if_exists='append', index=False)


    del CNN_bigrams_df
    del bigrams_df_temp
    del words_df_temp
    del trigrams_df_temp

sql_query = pd.read_sql_query('''select*from CNN_test ''',conn)
c = conn.cursor()
c.execute('.open pythonsqlite.db')

que=pd.read_sql_query('''SELECT*FROM CNN_test
                            LIMIT 100; ''',conn)

x="'ACD'"
                        
acd_phrases=pd.read_sql_query('''SELECT Phrase
                                 FROM CNN_test
                                 WHERE Speaker='''+str(x)+'''
                                 LIMIT 1200;''',conn)
                                                  
                        
dates=pd.read_sql_query('''SELECT DISTINCT Date
                                 FROM scrape_test_bigrams;
                                 ''',conn)

dates=list(dates['Date'])

speakers=pd.read_sql_query('''SELECT DISTINCT Speaker
                                 FROM scrape_test_bigrams;
                                 ''',conn)

speakers=list(speakers['Speaker'])                


                           
que=pd.read_sql_query('''SELECT*FROM scrape_test_bigrams
                            LIMIT 10000; ''',conn)
                            
bigrams_df=pd.DataFrame()

phrases=pd.read_sql_query('''SELECT Phrase, COUNT(*)
                             FROM scrape_test_bigrams
                             GROUP BY Phrase
                             HAVING COUNT(*)>29''', conn)
                             
words=pd.read_sql_query('''SELECT Word, COUNT(*)
                             FROM scrape_test_words
                             GROUP BY Word
                             HAVING COUNT(*)>29''', conn)

sql = 'DELETE FROM scrape_test_trigrams'
cur = conn.cursor()
cur.execute(sql)
conn.commit()
                             

phrases=list(phrases['Phrase'])

getout=["('ð', '\\x9f\\x93±')"]
phrases = list(filter(lambda phrase: phrase not in excluded_bigrams, phrases))                    
words = list(filter(lambda phrase: phrase not in excluded_bigrams, phrases))


bigrams_df=pd.DataFrame()

#Rearrange
for i in range(len(speakers)):
    
    speaker=speakers[i]
    speaker ="'"+speaker+"'"
    if i==0:
        print("Building Bigram Counts. Progress:")
    x=str(((i/(len(speakers))*100)))
    print(x[:4])
    df1=pd.DataFrame()
    df1= pd.read_sql_query('''SELECT*FROM CNN_bigrams
                              WHERE Speaker='''+speaker+''';''',conn)
    
    
    dates=set(list(df1['Date']))
    dates=list(dates)
    
    bigrams_temp=pd.DataFrame()
    for j in range(len(dates)):
        
        df2=df1[df1['Date']==dates[j]]
        phrase_count=df2['Phrase'][df2['Phrase'].isin(phrases)].value_counts(ascending=True)
        phrase_count=pd.DataFrame(phrase_count)
        
        phrase_count=pd.DataFrame.transpose(phrase_count)
        phrase_count.insert(0, "Speaker", speakers[i], True)
        phrase_count.insert(1, "Date", dates[j], True)
        phrase_count.insert(2, "Network", dates[j], True)
        bigrams_temp=pd.concat([bigrams_temp,phrase_count])
    
    bigrams_df=pd.concat([bigrams_df,bigrams_temp])                            
    del bigrams_temp                        
                            
bigrams_df=bigrams_df.fillna(0)

