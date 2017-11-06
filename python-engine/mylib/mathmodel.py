





# For now normalization seems like the most accurate method
def normalizeDict(adict, method='raw'):

	return_dict = {}
	value_lst = []
	mean = None


	#this is for just outputing the raw values of the count
	if method == 'raw':
		return adict

	'''Regular normalization, i grab the max then multiply by 100 to get
	the % of popularity compared to the most popular item in the given data'''
	if method == 'max':

		noe = False

		for key, value in adict.items():
			value_lst.append(value)

		for key, value in adict.items():
			return_dict[key] = int((value/max(value_lst))*100)

		# print(max(value_lst))

		return return_dict

	'''Normalizes the data based on the % it takes of the total amount of data
	in the sense that every value added together will add up to 1, meaning
	im getting how popular it is in general as well'''

	if method == 'sum':

		for key, value in adict.items():
			value_lst.append(value)

		for key, value in adict.items():
			return_dict[key] = int((value/sum(value_lst))*100)
			# print(return_dict[key])
			# print(sum(value_lst))

		return return_dict


	raise Exception('Method Error: the method passed to function normalizeDict is invalid!')









