import sys
import json
import operator
# my libs
import mylib.timedata as timedata
from mylib.timedata import get_time_in_seconds
import mylib.dataHandler as dataH 
import mylib.mathmodel  as mathmodel


# temp 
import time 



# =======================================
# GLOBALS

DEBUG = False

output_data = "output_main.txt"
the_db = 'jsondata.txt'
keyword = None

# =======================================


# prints data if in debug mode 
def dprint(data):
	if DEBUG:
		print("DEBUG: {}".format(str(data)))





# establish communication with pika to get the json
def load_data():
	tweet = ''

	try:
		encoded_json = body.decode('ascii', 'ignore')
		tweet = encoded_json
	except Exception as e:
		print(e)


	return tweet


# responsible for loading in the data from either a text file or a json file into a list of dicts
def readFile(filename):
	extension = filename.split('.')[1]

	#read everything into a list of dictionaries
	dic_array = []

	if extension == 'txt':
		with open(filename, 'r') as file:
			for line in file:
				dic_array.append(json.loads(line))

	return dic_array


def get_valuables(data_array):

	mentions_count = {}
	url_count = {}
	hashtags_count = {}
	media_count = {}
	retweet_id_count = {}

	for data in data_array:

		# get worth of the data

		points = timedata.points_gen(data)


		#MENTIONS
		try:
			mentions = [data['entities']['user_mentions'][i]['screen_name'] for i in range(len(data['entities']['user_mentions']))]
			
			for item in mentions:
				try:
					mentions_count[item] += points
				except KeyError:
					mentions_count[item] = points
		except KeyError:
			dprint('No mentions')

		#URLS
		try:
			user_urls = [data['entities']['urls'][i]['expanded_url'] for i in range(len(data['entities']['urls']))]

			for url in user_urls:
				try:
					url_count[url] += points
				except KeyError:
					if url:
						url_count[url] = points
		except KeyError:
			dprint('No urls')

		#HASTAGS
		try:
			user_hashtags = [data['entities']['hashtags'][i]['text'] for i in range(len(data['entities']['hashtags']))]

			for hashtag in user_hashtags:
				try:
					if hashtag.lower() != keyword:       # avoid getting the same hashtag for the keyword youre looking for
						hashtags_count[hashtag] += points
				except KeyError:
					hashtags_count[hashtag] = points
		except KeyError:
			dprint('No hashtags')


		#MEDIA
		#COME BACK TO THIS WHEN RELEVANT


		# IN THE CASE OF A RETWEET (this is where the except catcher will be usefull as not all tweets are retweets)
		try:
			retweet_id =data['retweeted_status']['id_str']
			retweet_fav_count = data['retweeted_status']['favorite_count']
			retweet_retweet_count = data['retweeted_status']['retweet_count']

			created_at = data['retweeted_status']['created_at'].split(' ')[3] # exmpl "Fri Jun 30 15:17:32 +0000 2017"
			created_at = get_time_in_seconds(created_at)

			# need a way to locate important data 

		except KeyError:
			dprint('Tweet is not a retweet')

	return mentions_count, hashtags_count, url_count

def get_top(dic_count, title='', num_method='raw'):
	#RIGHT HERE
	# i might want to do the point thing but thats later on when im working on 
	# the javafx launcher which will have to seem to do the job

	# this is where chenge the input from the javafx launcher
	#set a default value
	d_method = "raw"

	if num_method == "2":
		d_method = "max"
	elif num_method == "3":
		d_method = "sum"


	normalized = mathmodel.normalizeDict(dic_count, method=d_method) # normalizes the numbers
	readable_count = dataH.getReadable(normalized)	# fixes the encoding for the output to be readable
	sorted_count = sorted(readable_count.items(), key=operator.itemgetter(1)) #sorts it to get the top dogs



	# clean the file

	top5 = sorted_count[:-6:-1] # gets top 5 (fix this later and allow a prompt to be passed)
	# print(top5)
	# top5 = [[key[0].encode('utf-8').decode('ascii', 'ignore') if not None else '' for key in top5]]

	# print('\nCount')
	# [print('Name: {0}, Count: {1}'.format(top5[i][0], top5[i][1])) for i in range(len(top5))]
	print('\n')

	with open(output_data, 'a') as File:

		File.write("{}:\n".format(title))

		for line in top5:
			data = line[0]
			print(data)
			count = line[1]

			if d_method=='raw':
				File.write("  {} --:  Score of: {}\n".format(data, count))
			elif d_method=='max':
				if count==100:
					File.write("  {} --:  This is the most popular\n".format(data, count))
				else:
					File.write("  {} --:  {}%  as popular compared to the most popular\n".format(data, count))

			elif d_method=='sum':
				if count==0:
					File.write("  {} --:  less than {}%  as popular compared to the most popular\n".format(data, count+1))
				else:
					File.write("  {} --:  {}%  of total tweets\n".format(data, count))
		File.write('\n\n')
		# print('\n\n')

		# [File.write("Str: {}; Count: {}\n".format(line[0].encode('utf-8').decode('ascii'), line[1])) for line in top5]
		# File.write('\n\n')


''' 
Funny thing is that most tweets going throught the stream are retweets, meaning that most of these people rather just agree with the
statement of someone else instead of making their own statement out of the informaton given, clearly it can just be that they don't 
want to be accused of copying someone elses idea
'''





with_counts = {}

def add_items(lst_items):
	global with_counts
	if lst_items:
		for mention in lst_items:
			try:
				with_counts[mention] += 1
			except KeyError:
				with_counts[mention] = 1

def setDBName(str_name):
	static_dir = "dbs/" # insert string to static dir loc
	new_name = static_dir + str_name + "json.txt"
	return new_name



# function that clears any old data from our 'database'
def initializer():
	curr_time = time.time()
	the_data = readFile(the_db)

	fresh_data = []

	# create a batch of tweets that are less than a week old
	for item in the_data:
		# temp_dict = json.loads(item)
		if dataH.is_old(item) == False: # if its still fresh
			fresh_data.append(item)

	new_batch = the_db.split('.')[0] + '2.txt' 

	# rewrite it to file, this is old and takes time, maybe read to the file first then 
	# load it into it
	with open(the_db, 'w') as File:
		for item in fresh_data:
			string = json.dumps(item) + '\n'
			File.write(string)

	print(time.time() - curr_time)


def main():

	global keyword
	global the_db

	# clean out main and leave message in case of error with the db access
	with open(output_data, 'w') as File:
		File.write("Keyword has not been searched or the database file as been corrupt")
	
	try:
		keyword = sys.argv[1]
		norm = str(sys.argv[2])
	except IndexError as e:

		# you could save this to the reader and have it display
		error_log1 = "An error has occured where the UI isn't communicating with the engine please inform the programmer"
		error_log2 = "Command line arguements aren\'t being passed"
		time_log = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())
		with open('errorlog.txt', 'a') as File:
			File.write(error_log1)
			File.write("\n" + error_log2)

	# set the currdb name
	# output_data = dataH.addtxt(keyword) # this becomes the new place
	the_db = setDBName(keyword)
	filename = the_db

	initializer()
	
	array = readFile(filename)

	ment, hashy, urls = get_valuables(array)

	# clean the file

	#clean it
	with open(output_data, 'w') as File:
		pass

	# print('Mentions')
	get_top(ment, 'Mentions (users)', norm)
	# print('Hashtags')
	get_top(hashy, 'Hashtags', norm)
	# print('Urls')
	get_top(urls, 'URLS', norm)


if __name__ == '__main__':
	# curr_time = time.time()
	main()
	time.sleep(1) # sleeping for a second to give time for the ui the grab the writing
	# print(time.time()-curr_time)