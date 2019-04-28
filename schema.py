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

#
def treat_dataframe(csv_file_path,delimiter='|'):
	with open(csv_file_path,'r') as csv_file_in:
		csv_in = csv.reader_dict(csv_file_in,delimiter=delimiter)
		with open(csv_file_path.replace('.csv','_tmp.csv'),'w') as csv_file_out:
			csv_out = csv.writer(csv_file_out.replace,delimiter=delimiter)
			# add method to replace values	
			[csv.writerow(next(csv_in) for _ in csv_in]

def gen_distinct_rows(csv_file_path):
	'''
	Reads a csv_file from the file_path and return the unique values of each column and the headers enumerated
	:param csv_file_path: string of the csv file path
	:return: a list of sets with the row values and a enumerated list of headers
	'''
	with open(csv_file_path, 'r') as file:
		reader = csv.reader(file, delimiter="|",quotechar='"')
		header = next(reader)
		list_unq= [set() for _ in list(range(0, len(header)))]
		for row in reader:
			[unq_set.add(row_val) for row_val,unq_set in zip(row, list_unq) if (row_val != '')]
		return list_unq,enumerate(header)


# Function that separate booleans and non booleans from a csv file
def separate_booleans(rows_set:list):
	'''
	Return two lists one with the values that are booleans others that are not
	:param rows_set: a list of sets with the value of each row
	:return: two lists one with the booleans other with other types
	'''
	rows_set = list(enumerate(rows_set))
	valid_bool = []
	not_valid= []
	for tup_ind in rows_set:
		set_val = tup_ind[1]
		if all((isinstance(val,int) and (val == 0 or val == 1)) or isinstance(val,bool) or (isinstance(val,str) and (val.lower() == 'true' or val.lower() =='false')) for val in set_val):
			valid_bool.append(tup_ind)
		else:
			not_valid.append(tup_ind)
	return valid_bool, not_valid






