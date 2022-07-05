from flask import Flask
import json 
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
invertedIndex = {}
    
class InvertedIndex(Resource):
    def get(self):
        return json.dumps(invertedIndex['data']), 200
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('invertedIndex', required=True)  # add args        
        args = parser.parse_args()  # parse arguments to dictionary
        invertedIndex['data'] = args['invertedIndex']
        
    
api.add_resource(InvertedIndex, '/') 

if __name__ == '__main__':
    app.run()  # run our Flask app