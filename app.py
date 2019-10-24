from flask import Flask, request, redirect
from flask_restful import Resource, Api
from auth import authenticator
from validator_collection import checkers
import json
from queryutil import execute_query
from utils import utils
import argparse
from sys import argv

app = Flask(__name__)
api = Api(app)

class CreateURL(Resource):
    """
    Class that manages the /create endpoint to create shortlinks
    """
    def put(self):
        auth = authenticator()
        if not auth.check_content_type(request.headers):
            return {'Error': 'Please provide your request in the json format.'}, 400
        if auth.check_key(request.headers):
            try:
                linkinfo = json.loads(request.data)
            except json.JSONDecodeError:
                return {'Error': 'Your JSON is invalid.'}, 400
            if not checkers.is_url(linkinfo["full_url"]):
                return {'Error': 'Your URL is not valid.'} , 400
            encoded_url = utils().encode_url(linkinfo["full_url"])
            shortlink = execute_query().store_record(encoded_url)
            if shortlink:
                return {'url': f'{shortlink}'}, 201
        return {'Error': 'Your key is invalid or missing.'}, 401

    def delete(self):
        pass

class GetURL(Resource):
    """
    Class to redirect users to the full url
    """
    def get(self, link_id: str) -> any:
        print(link_id)
        redirect_url = execute_query().get_url(link_id)
        print(redirect_url)
        if redirect_url:
            return redirect(utils().decode_url(redirect_url[0]), code=302)
        else:
            return {'Error': 'The entered shortlink is not present in our system.'}, 404


api.add_resource(CreateURL, '/create')
api.add_resource(GetURL, '/<string:link_id>')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--fresh-start", help="Runs DB fresh start creating the relative tables.", type=int)
    parser.add_argument("--create-api-key", help="Creates and returns an API key, please provide your email as argument.", type=str)
    parser.add_argument("--create-shortlink" , help="Creates a shortlink alias via commandline, provide a full URL as argument.", type=str)
    parser.add_argument("--server-start", help="Starts the server.", type=int)
    parser.parse_args()
    args = parser.parse_args()
    if args.fresh_start and args.fresh_start == 1:
        execute_query().create_default_tables()
        print("Database and tables created.")
    if args.create_api_key:
        if checkers.is_email(args.create_api_key):
            print(execute_query().add_api_key(args.create_api_key))
        else:
            print('Please provide a valid email.')
    if args.create_shortlink:
        if checkers.is_url(args.create_shortlink):
            print(execute_query().store_record(args.create_shortlink))
    if args.server_start and args.server_start == 1:
        app.run(host='127.0.0.1', debug=True, port=80, use_reloader=True)
    if not len(argv) > 1:
        # No arguments were passed, switch to default behaviour
        parser.print_help()