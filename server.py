from flask import Flask, request, jsonify
import json 
from flask_cors import CORS
import os
from os.path import exists

BASE_PATH = os.path.abspath(os.getcwd())
app = Flask(__name__)
CORS(app)
invertedIndex = {'data': {}}
file_exists = exists("INVERTED-INDEX.txt")

if file_exists:
    inverted_index = open(f"{BASE_PATH}/INVERTED-INDEX.txt", "r", encoding="utf-8").read()
    invertedIndex['data'] = inverted_index

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
    try:
        postingList = json.loads(invertedIndex['data'])[query]
        return jsonify({"docs": postingList})
    except:
        return "Term not found!"


if __name__ == '__main__':
    app.run()  # run our Flask app