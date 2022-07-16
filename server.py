from flask import Flask, request, jsonify
import json 
from flask_cors import CORS
import os
from os.path import exists
from hazm import *
from unidecode import unidecode

BASE_PATH = os.path.abspath(os.getcwd())
app = Flask(__name__)
CORS(app)
invertedIndex = {'data': {}}
file_exists = exists("INVERTED-INDEX.txt")

if file_exists:
    inverted_index = open(f"{BASE_PATH}/INVERTED-INDEX.txt", "r", encoding="utf-8").read()
    invertedIndex['data'] = inverted_index


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

def normalizeQuery(query):
    normalizer = Normalizer()
    stemmer = Stemmer()
    normalize = normalizer.normalize(query)
    stem = stemmer.stem(normalize)
    tokenize = word_tokenize(stem)
    lemmatizeList = lemmatize(tokenize)
    return omitStopWordsAndElims(lemmatizeList)

def Or(list1,list2):      
    ListA = list() 
    for x in list1: 
        ListA.append(x) 
        for y in list2: 
            if(x != y): 
                ListA.append(y) 
     
    return list(set(ListA)) 
 
 
def And(list1,list2):      
    ListA = list() 
    for x in list1: 
        for y in list2: 
            if(x == y): 
                ListA.append(x) 
     
    return ListA

@app.route('/', methods=["GET"])
def getInvertedIndex():
    return jsonify(invertedIndex['data']), 200

@app.route('/', methods=["POST"])
def setInvertedIndex():
    invertedIndex['data'] = request.get_json(force=True)['invertedIndex'] 
    return "success"

@app.route('/search', methods=["POST"])
def searchQuery():
    query= request.get_json(force=True)['query']
    normal_query = normalizeQuery(query)
    try:
        if len(normal_query) <= 2:
            try:
                postingList = json.loads(invertedIndex['data'])[normal_query[0]]
            except: 
                postingList = json.loads(invertedIndex['data'])[query]
            return jsonify({"docs": postingList})
        else:
            if "AND" in normal_query or "and" in normal_query:
                if "and" in normal_query:
                    and_position = normal_query.index("and")
                else: 
                    and_position = normal_query.index("AND")
                postingList = And(json.loads(invertedIndex['data'])[normal_query[and_position-1]], json.loads(invertedIndex['data'])[normal_query[and_position+1]])
                return jsonify({"docs": postingList})
            if "OR" in normal_query or "or" in normal_query:
                if "or" in normal_query:
                    OR_position = normal_query.index("or")
                else: 
                    OR_position = normal_query.index("OR")              
                postingList = Or(json.loads(invertedIndex['data'])[normal_query[OR_position-1]], json.loads(invertedIndex['data'])[normal_query[OR_position+1]])
                return jsonify({"docs": postingList})          
    except:
        return "Term not found!"


if __name__ == '__main__':
    app.run()  # run our Flask app