import mysql.connector
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

import numpy as np
import random
import string
import _pickle as pickle


import urllib.request
import re

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456",
  database= "data_analysis"
)



#Fetch Processed_Data Columns from the DataBase

mycursor = mydb.cursor()
sql = 'Select Processed_Data from QA_1'

mycursor.execute(sql)
myresult = mycursor.fetchall()
text_string= ''
for x in myresult:
    text_string+=x[0]

#"sent_tokenize" function from the NLTK library is used to split the corpus into individual sentences.
corpus = nltk.sent_tokenize(text_string)

#Removing Spaces and punctuations from the Corpus (Corpus is the collection of words)
for i in range(len(corpus)):
    corpus [i] = corpus [i].lower()
    corpus [i] = re.sub(r'\W',' ',corpus[i])
    corpus [i] = re.sub(r'\s+',' ',corpus[i])





"""
Creating a dictionary that will contin the words with frequency
"""
wordfreq = {}
for sentence in corpus:
    #tokens contains words, The sentences i corpus are broken ito words and stored in the tokens
    tokens = nltk.word_tokenize(sentence)

    #Remove the stopwords from the tokens and store in  tokens_without_sw
    tokens_without_sw = [word for word in tokens if not word in stopwords.words('english')]

    #Now from  tokens_without_sw store in dic, if token not in wordfreq add the word with frequency 1 otherwise if it already exists that increase the count by one
    for token in tokens_without_sw:
        if token not in wordfreq.keys():
            wordfreq[token] = 1
        else:
            wordfreq[token] += 1

"""
printing dictionary by key : value
"""
# for key, value in wordfreq.items ():
#     print(key, ' : ', value)

"""
Sorting by key
"""
for i in sorted (wordfreq):
    print (i, ' : ',wordfreq[i])



"""
sort by value
"""
# sort_dict=sorted(wordfreq.items(),key=lambda  x: x[1], reverse=True)
# for i in sort_dict:
#     print(i[0],i[1])

