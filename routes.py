from flask import Flask, request, redirect
from flask_restful import Resource, Api
from auth import authenticator
from validator_collection import checkers
import json
from queryutil import execute_query
from utils import utils

app = Flask(__name__)
api = Api(app)

class ApiManager(Resource):
    """
    This class will manage api tasks like adding an api key
    or deleting/changing permission to a specific user. ]
    @Todo: Filippo
    """
    def get(self):
        pass
    def put(self):
        pass

class CreateURL(Resource):
    """
    Class that manages the /create endpoint to create shortlinks
    """
    def put(self):
        auth = authenticator()
        if not auth.check_content_type(request.headers):
            return { 'Error' : 'Please provide your request in the json format.' }, 401
        if auth.check_key(request.headers):
            linkinfo = json.loads(request.data) 
            if not checkers.is_url(linkinfo["full_url"]):
                return {'Error' : 'Your URL is not valid.'} , 401
            encoded_url = utils().encode_url(linkinfo["full_url"])
            shortlink = execute_query().store_record(encoded_url)
            return {'url' : f'{shortlink}'}, 201
        return { 'Error' : 'Your key is invalid or missing.' }, 401

    def delete(self):
        pass

class GetURL(Resource):
    """
    Class to redirect users to the full url
    """
    def get(self, link_id: str) -> any:
        redirect_url = execute_query().get_record(link_id)
        if redirect_url:
            return redirect(utils().decode_url(redirect_url[0]), code=302)
        else:
            return {'Error' : 'The entered shortlink is not present in our system.'}, 404

api.add_resource(CreateURL, '/create')
api.add_resource(GetURL, '/<string:link_id>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=80, use_reloader=True)