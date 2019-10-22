from queryutil import execute_query
from re import match as regexmatch


class authenticator:

    def check_key(self, header):
        try:
            if header['x-api-key']:
                if regexmatch(r'^[A-Za-z0-9]{24}$', header['x-api-key']):
                    if execute_query().check_api_key(header['x-api-key']):
                        return True
            return False
        except KeyError:
            return False

    def check_content_type(self, header):
        try:
            if header['Content-Type'] == 'application/json':
                return True
            return False
        except KeyError:
            return False
