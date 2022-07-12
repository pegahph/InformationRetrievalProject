from __future__ import unicode_literals
from pickle import APPEND
from hazm import *
import os
import json 
import requests
import webbrowser
from unidecode import unidecode
BASE_PATH = os.path.abspath(os.getcwd())
path = BASE_PATH + "/txtfiles"
os.chdir(path)

invertedIndex_dict = {}



def updateInvertedIndex(list, docId):
    for i in list:
        if i in invertedIndex_dict.keys():
            if docId not in invertedIndex_dict[i]:                
                invertedIndex_dict[i].append(docId)
        else:
            invertedIndex_dict[i] = [docId]

def omitStopWordsAndElims(list):
    modifiedList = []
    stopWords = open(f"{BASE_PATH}/project_files/stop.txt", "r", encoding="utf-8").read()
    elims = open(f"{BASE_PATH}/project_files/elim.txt", "r", encoding="utf-8").read()
    for i in list:
        if i.isnumeric()== True :
            modifiedList.append(unidecode(i))
        if i not in stopWords and i not in elims:
            modifiedList.append(i)
    return modifiedList


def lemmatize(tokenList):
    lemmatizer = Lemmatizer()
    lemmatizeList = []
    for word in tokenList:
        lemmatizeList.append(lemmatizer.lemmatize(word))
    return lemmatizeList

  

      
for file in os.listdir():
    docId = file.replace(".txt","")
    # docId = file.removesuffix(".txt")
    file_path =f"{path}/{file}"
    with open(file_path, 'r', encoding="utf-8") as file:
        normalizer = Normalizer()
        stemmer = Stemmer()
        normalize = normalizer.normalize(file.read())
        stem = stemmer.stem(normalize)
        tokenize = word_tokenize(stem)
        lemmatizeList = lemmatize(tokenize)
        updateInvertedIndex(omitStopWordsAndElims(lemmatizeList), docId)

response = requests.post("http://127.0.0.1:5000", json = {'invertedIndex': json.dumps(invertedIndex_dict)})
webbrowser.get('chrome').open('file://' + BASE_PATH + '/index.html')
# webbrowser.get('windows-default').open('file://' + BASE_PATH + '/index.html')
  