import tweepy
import sys
import json

import staticdata.keys as sk

# ==========================================
# GLOBALS

key = sk.key
secret = sk.secret

access_token = sk.access_token
a_token_secret = sk.a_token_secret


the_db = 'jsondata.txt'

# ==========================================

class MyStreamListener(tweepy.StreamListener):
	def __init__(self, api):

		# initialize the needs of the base class
		super(tweepy.StreamListener, self).__init__()
		self.api = api

		

	def on_status(self, status):
		
		if status.lang == 'en':
			# print(status.retweet)
					
			json_str = json.dumps(status._json)


			# send just the text since it's the only indicator needed
			# single_line = clean_data(status.text)
			
			with open(the_db, 'a') as File:
				File.write(json_str.encode('utf8').decode('ascii', 'ignore') + '\n')

			# self.channel.basic_publish(exchange='', routing_key=queue_name, body=json_str)

	def on_error(self, status_code):
		print('Encountered error with status code: {}'.format(status_code), file=sys.stderr)
		return True  # Don't kill the stream

	def on_timeout(self):
		print('Timeout...', file=sys.stderr)
		return True  # Don't kill the stream



def _login():
	# login data
	auth = tweepy.OAuthHandler(key, secret)
	auth.set_access_token(access_token, a_token_secret)

	api = tweepy.API(auth)

	return auth,api

def setDB(str_name):
	global the_db
	the_db = "dbs/" + str_name + "json.txt"


def init_stream(keywrd):
	
	w_auth, w_api = _login()
	listener = MyStreamListener(w_api)     # UPDATED LATER
	stream = tweepy.Stream(w_auth, listener)

	stream.filter(track = list(keywrd))


def main():

	try:
		search_kewrd = sys.argv[1]
		d_list = search_kewrd.split(',')
		setDB(d_list[0].lower())
		init_stream(d_list)
	except IndexError:
		print('No arguments where passed killing process')
		sys.exit(1)

	init_stream()

if __name__ == '__main__':
	main()