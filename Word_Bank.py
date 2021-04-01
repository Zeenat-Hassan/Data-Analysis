import mysql.connector
import nltk
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




mycursor = mydb.cursor()
sql = 'Select Processed_Data from QA_1'

mycursor.execute(sql)
myresult = mycursor.fetchall()
text_string= ''
for x in myresult:
    text_string+=x[0]
#print(text_string)

corpus = nltk.sent_tokenize(text_string)

for i in range(len(corpus)):
    corpus [i] = corpus [i].lower()
    corpus [i] = re.sub(r'\W',' ',corpus[i])
    corpus [i] = re.sub(r'\s+',' ',corpus[i])

print(len(corpus))
#print(corpus[1])

wordfreq = {}
for sentence in corpus:
    tokens = nltk.word_tokenize(sentence)
    for token in tokens:
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
# for i in sorted (wordfreq):
#     print (i, ' : ',wordfreq[i])

"""
Writing into text file
"""
# f = open("fl.txt", "a")
# data = str(wordfreq)
# f.write(data)

"""
sort by value
"""
sort_dict=sorted(wordfreq.items(),key=lambda  x: x[1], reverse=True)
for i in sort_dict:
    print(i[0],i[1])
