import json
import mylib.timedata as td



# function specific for twitter json
def is_old(json_obj):

	# 1 week == 604800 seconds

	week = 604800
	time_alive = td.get_time_since(json_obj)

	if time_alive > week:
		return True
	else:
		return False


'''
this function will go throught the data and use some unicode conversion
ignoring anything that cant be translated into ascii
if the output is an empty string the language is far from being important 
in the US, therefore it should just be ignored
'''
def getReadable(adict):
	return_dict = {}

	for key, value in adict.items():
		tempkey = key.encode('utf-8').decode('ascii', 'ignore')

		# if it isnt an empty string or a space we can pass it on to be exposed
		if tempkey!='' or tempkey !=' ':
			return_dict[tempkey] = value

	return return_dict



# just an enum type method for cleaning up the input in main





# this will generate the points based on a few things
# ok so we're parsing the data individiually and checking certain things
# 1. Data from the last hour and today are more relevant
# 2. Data from the same user loses it's value up to a threshhold

def getPoints(json_obj):

	def threshold(amin, amax):
		pass


	for key, value in json_obj.items():
		pass

# adds txt and later the static loc for dbs
def addtxt(string):
	return string + ".txt"








