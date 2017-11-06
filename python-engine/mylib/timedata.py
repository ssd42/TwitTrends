import time


#NOTE this funciton is irrelevant now

# quick fix over using datetime which has all of those wierd formatting
# that numpy isnt alway cool with
def get_time_in_seconds(time_string):

	time = time_string.split(':')
	time = [int(num) for num in time]


	# total time = 3600 * hours + 60 * minutes + seconds
	total_time = (3600*time[0])+(60*time[1]) + time[2]

	return total_time


def get_time_since(tweet_obj):

	# get the cureent unix time
	tweet_time = int(tweet_obj['timestamp_ms'])
	curr_time = time.time()

	passed_time = curr_time - tweet_time

	'''
	seconds in an hour = 60*60 = 3600
	seconds in a day = 24*60*60 = 86400
	seconds in 2 days = 2 * secs_day = 172800
	seconds in 3 days = 3 * secs_day = 259200
	seconds in a week = 7 * secs_day = 604800

	Ignore everything else
	'''

	# for now just return the time figure out the reating system later
	return passed_time
	
'''
Points System for now
Last hour: 5
Last Day: 3
last week: 1

Try this to keep most relevant afloat
'''




def points_gen(tweet_obj):
	# Time worth
	last_hour = 5
	last_day = 3
	last_week = 1


	tm_alive = get_time_since(tweet_obj)

	if tm_alive <= 3600: # an hour
		return last_hour
	elif tm_alive <= 86400: # a day
		return last_day
	else:
		return last_week





