from __future__ import unicode_literals
from hazm import *
import os, sys, time
import json 
import requests
import webbrowser
from os.path import exists
import glob
from subprocess import call

BASE_PATH = os.path.abspath(os.getcwd())

invertedIndex_dict = {}



def updateInvertedIndex(list, docId):
    for i in list:
        if i in invertedIndex_dict.keys():
            if docId not in invertedIndex_dict[i]:                
                invertedIndex_dict[i].append(docId)
        else:
            invertedIndex_dict[i] = [docId]
        invertedIndex_dict[i].sort()

def omitStopWordsAndElims(list):
    modifiedList = []
    stopWords = open(f"{BASE_PATH}/project_files/stop.txt", "r", encoding="utf-8").read()
    elims = open(f"{BASE_PATH}/project_files/elim.txt", "r", encoding="utf-8").read()
    for i in list:
        if i not in stopWords and i not in elims:
            modifiedList.append(i)
    return modifiedList


def lemmatize(tokenList):
    lemmatizer = Lemmatizer()
    lemmatizeList = []
    for word in tokenList:
        lemmatizeList.append(lemmatizer.lemmatize(word))
    return lemmatizeList
   
def tokenizeAndCreateInvertedIndex(file):
    normalizer = Normalizer()
    stemmer = Stemmer()
    normalize = normalizer.normalize(file.read())
    stem = stemmer.stem(normalize)
    tokenize = word_tokenize(stem)
    lemmatizeList = lemmatize(tokenize)
    updateInvertedIndex(omitStopWordsAndElims(lemmatizeList), docId)

os.chdir(BASE_PATH)
file_exists = exists("INVERTED-INDEX.txt")
if file_exists:
    pass
else:
    path = BASE_PATH + "/txtfiles"
    os.chdir(path)
    for file in os.listdir():
        docId = int(file.removesuffix(".txt"))
        file_path =f"{path}/{file}"
        with open(file_path, 'r', encoding="utf-8") as file:
            normalizer = Normalizer()
            stemmer = Stemmer()
            normalize = normalizer.normalize(file.read())
            stem = stemmer.stem(normalize)
            tokenize = word_tokenize(stem)
            lemmatizeList = lemmatize(tokenize)
            updateInvertedIndex(omitStopWordsAndElims(lemmatizeList), docId)

    os.chdir(BASE_PATH)
    f = open("INVERTED-INDEX.txt", "x")
    f = open("INVERTED-INDEX.txt", "w")
    f.write(json.dumps(invertedIndex_dict))
    f.close()

    response = requests.post("http://127.0.0.1:5000", json = {'invertedIndex': json.dumps(invertedIndex_dict)})


folder_path = f"{BASE_PATH}/txtfiles"
file_type = r'/*.txt'
files = glob.glob(folder_path + file_type)
last_file = max(files, key=os.path.getctime)

webbrowser.get('windows-default').open('file://' + BASE_PATH + '/index.html')

try:
    while True:
        files = glob.glob(folder_path + file_type)
        max_file = max(files, key=os.path.getctime)
        if last_file != max_file :
            last_file = max_file
            print("inverted index should be update")
        time.sleep(4)

except KeyboardInterrupt:
    pass


  