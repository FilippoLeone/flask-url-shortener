import string
import random
import urllib.parse
import re

class utils:
    def generate_string(self, length=8, type=None):
        return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length))

    def encode_url(self, url):
        return urllib.parse.quote(url)

    def decode_url(self, url):
        return urllib.parse.unquote(url)