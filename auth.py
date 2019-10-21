from queryutil import execute_query
from re import match as regexmatch

class authenticator:

    def check_api_key(self, header):
        if header['api-key']:
            if regexmatch(r'^[A-Za-z0-9]{24}$', header['api-key']): # Validating key format and size
                if execute_query().check_api_key(header['api-key']):
                    return True
        return False
