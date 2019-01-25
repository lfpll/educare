import csv
import re
from os import remove as remove_file

# Class that define a file type of a string for generating DB's schema
class Define_type:
	def __init__(self,min_year= 1900):
		date_string = "^([3][0-1]|[0-2][0-9])/([1][0-2]|0?[1-9])/[%s-2019]$" %str(min_year)
		self.date_regex  = re.compile(date_string)
		self.int_regex = re.compile("^[0-9]+$")
		self.float_regex = re.compile("^([0-9]+)?\.[0-9]+$")

	# Function that receives a string and define the type
	def classify_string(self,string):
		if isinstance(string,str):
			if self.date_regex.search(string):
				return 'DATETIME'
			elif self.int_regex.search(string):
				return "INTEGER"
			elif self.float_regex.search(string):
				return "FLOAT"
			else:
				return "STRING"
		else:
			raise('File type is not attribute string '%string)


# Return a list of sets with the unique values of each row in a csv
def gen_distinct_rows(file_name):
	with open(file_name,'r') as file:
		reader = csv.reader(file, delimiter="|",quotechar='"')
		header = next(reader)
		list_unq= [set() for _ in list(range(0, len(header)))]
		for row in reader:
			[unq_set.add(row_val) for row_val,unq_set in zip(row, list_unq) if (row_val != '')]
		return list_unq,enumerate(header)


# Fuction that separate booleans and non booleans from a csv file
def separate_booleans(rows_set:list):
	'''
	Input: List of lists (list of rows)
	Output: two list of sets
			- valid_bool: rows that can be transformed to booleans
			- not_valid: rows that can't\shouldn't be transformed to booleans
	'''
	rows_set = list(enumerate(rows_set))
	valid_bool = []
	not_valid= []
	for tup_ind in rows_set:
		set_val = tup_ind[1]
		if len(set_val) > 2:
			not_valid.append(tup_ind)
		elif any(len(val)>1 for val in set_val):
			not_valid.append(tup_ind)
		else:
			valid_bool.append(tup_ind)
	return valid_bool, not_valid


# TODO implement verification of types
# Converted enumerated set to boolean
def convert_to_boolean(enum_sets):
	'''
	Input: list of enumerated sets
		- enum_sets: [(1,set([1,2]}),....,(n,set([0,1]))]
	OutPut: converted enumerated set do boolean
	:   - convert_ref: [(1,set([True;False]),....,(n,set([True;False]))]
	'''
	convert_ref = []
	for index,row_set in enum_sets:
		if len(row_set) >0:
			row_set = iter(row_set)
			ref_dict = {next(row_set): 1}
			next_val = next(row_set, False)
			if next_val:
				ref_dict[next_val] = 0
			convert_ref.append((index,ref_dict))
	return convert_ref


# TODO implement verification of types
# Transform values of a csv to boolean based on enumerated list
def convert_csv_to_bool(file_path, bool_set_reference,remove=False):
	"""
	Function that receives the enumerated columns that can be transformed to booleans and convert then
	:param file_path: path of the csv file
	:param bool_set_reference: list of enumerated sets
	:param remove: if true remove original file
	:return: True if no error.
	"""
	writer_file = open(file_path[:-4] + '_converted.csv', 'w',newline='')
	writer = csv.writer(writer_file, delimiter=",")
	with open(file_path, 'r',newline='') as in_file:
		reader = csv.reader(in_file,delimiter="|")
		for row in reader:
			for index,bool_dict in bool_set_reference:
				if row[index] != '': row[index] = (bool_dict[row[index]])
			writer.writerow(row)
	if remove:
		remove_file(file_path)
	return True








