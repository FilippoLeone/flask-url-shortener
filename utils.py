import string
import random
import urllib.parse
import re
from datetime import datetime
from os import getcwd

class utils:
    def generate_string(self, length=8, type=None):
        return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length))

    def encode_url(self, url):
        return urllib.parse.quote(url)

    def decode_url(self, url):
        return urllib.parse.unquote(url)


class logger:
	def __init__(self):
		self.logfile = getcwd() + '/error_log.txt'

	def log_error(self, **kwargs):
		for errorcode, errormessage in kwargs.items():
			try:
				with open(self.logfile, 'a') as Logfile:
					Logfile.write(f"{datetime.now()} --- {errorcode} : {errormessage}\n")
			except FileNotFoundError:
				with open(self.logfile, 'w') as Logfile:
					Logfile.write(f"{datetime.now()} --- {errorcode} : {errormessage}\n")
