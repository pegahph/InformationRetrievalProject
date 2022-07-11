from flask import Flask, Response, make_response
import json 
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
invertedIndex = {'data': {}}
    

class InvertedIndex(Resource):
    def get(self):
        return json.dumps(invertedIndex['data']), 200, {"Access-Control-Allow-Origin": "*"}
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('invertedIndex', required=True)  # add args        
        args = parser.parse_args()  # parse arguments to dictionary
        invertedIndex['data'] = json.loads(args['invertedIndex'])

class Search(Resource):
    def post(self):
        resp = make_response()
        resp.headers.extend({"Access-Control-Allow-Origin": "*"})
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('query', required=True)  # add args  
        args = parser.parse_args()  # parse arguments to dictionary
        print(args)
        return args, 200


api.add_resource(InvertedIndex, '/') 
api.add_resource(Search, '/search')  

if __name__ == '__main__':
    app.run()  # run our Flask app