from typing import List

from schema import classify_csv
from table_converter import change_headers,convert_schema
from os import remove
import pytest

sample_data = [
	['FIRST', 'SECOND', 'THIRD', 'FOURTH', 'FIFTH'],
	[1, 2, 3, 4, 5],
	['TRUE', 2, 3, 4, 5],
	[0, 'AEAEAE', 3, 4, 5],
	['FALSE', 2, '02/04/2018', '4.56', 5],
	[1, 'TESTE', '30/12/1990', 4.56, 299]
]


response = {'FIRST': 'BOOLEAN',
			'SECOND': 'STRING',
			'THIRD': 'DATETIME',
			'FOURTH': 'FLOAT',
			'FIFTH': 'INTEGER'}

# Test csv assertion
def test_csv_assertion():
	with open('./tmp.csv', 'w') as file:
		map(file.write, sample_data)
	assert response == classify_csv('./tmp.csv')
	remove('./tmp.csv')


original_schema = {
	'ONE': 'INTEGER',
	'TWO': 'BOOLEAN',
	'THREE': 'STRING'
}

conv_patt = {
	'ONE': 'UM',
	'TWO': 'DOIS',
	'THREE': 'TRES'
}
expected_schema = {
	'UM': 'INTEGER',
	'DOIS': 'BOOLEAN',
	'TRES': 'STRING'
}

ref_schema = {
	'UM': 'INTEGER',
	'DOIS': 'BOOLEAN',
	'TRES': 'STRING'
}

wrong_ref_schema = {
	'UM': 'INTEGER',
	'DOIS': 'BOOLEAN',
	'TRES': 'BOOLEAN'
}

key_error_schema = {
	'ONE': 'INTEGER',
	'TWO': 'BOOLEAN',
	'THREE': 'STRING',
	'FOUR':'STRING'
}



# Test conversion of the csv header
def test_conversion_schema():
	assert expected_schema == convert_schema(schema=original_schema,
											 conversion_pattern=conv_patt,ref_schema=ref_schema)
	message_extra_key = 'Invalid key FOUR on the schema translation'
	message_dif_type = 'Diferent data type for THREE converted to 3, STRING expected BOOLEAN'
	with pytest.raises(KeyError):
		convert_schema(schema=key_error_schema,conversion_pattern=conv_patt,
					   ref_schema=ref_schema)
		exec(message_extra_key)
	with pytest.raises(ValueError):
		convert_schema(schema=original_schema,conversion_pattern=conv_patt,
					   ref_schema=wrong_ref_schema)
		exec(message_dif_type)



import csv
import os


original_table = [['ONE', 'TWO', 'THREE'],
				  ['DUM1', 'DUM2', 'DUM3'],
				  ['DUM1', 'DUM2', 'DUM3'],
				  ['DUM1', 'DUM2', 'DUM3']]




# Create a csv file from a matrix on list format
def gen_tmp_table(table:List[List[str]],table_name:str):

	parent_folder = os.path.dirname(os.path.abspath(__file__))+'/'
	tmp_file_path = parent_folder + table_name + '.csv'

	# Transforms table into csv file
	def create_table(file_path:str,table:list):
		if os.path.isfile(file_path):
			raise FileExistsError("%s already exists "%file_path)
		with open(file_path,'w') as tmp_file:
			writer = csv.writer(tmp_file)
			[writer.writerow(row) for row in table]
		return file_path

	create_table(file_path=tmp_file_path,table=table)
	return tmp_file_path

table_expected  = [['UM', 'DOIS', 'TRES'],
				  ['DUM1', 'DUM2', 'DUM3'],
				  ['DUM1', 'DUM2', 'DUM3'],
				  ['DUM1', 'DUM2', 'DUM3']]


table_error = [['ONE', 'FOUR', 'THREE'],
			  ['DUM1', 'DUM2', 'DUM3'],
			  ['DUM1', 'DUM2', 'DUM3'],
			  ['DUM1', 'DUM2', 'DUM3']]


# Rename the table file
def test_conversion_header():

	orig_table = gen_tmp_table(table=original_table, table_name='origin')
	change_headers(csv_input_path=orig_table, conversion_pattern=conv_patt)
	with open(orig_table,'r') as csv_file:
		csv_table =csv.reader(csv_file)
		csv_table = [row for row in csv_table]
		assert  csv_table == table_expected
	with pytest.raises(KeyError):
		table_error_path = gen_tmp_table(table=table_error,table_name='expected')
		change_headers(csv_input_path=table_error_path, conversion_pattern=conv_patt)
		message = "Value for FOUR not found in conversion"
		exec(message)
	os.remove(table_error_path)
	os.remove(orig_table)



