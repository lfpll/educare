from treat_data.convert import xlsx_to_csv,rewrite_csv
# What It does have to do!
'''
There is multiple files in csv and xlsx
1 - List all files
	1.1 - Select a specific path
	1.2 - If they are XLSX they have to converted do csv and append to paths
	1.3 - If they are csv add to lists
	1.4 - Else raise error
2 - Run the table script on the paths
	2.1 - Get the schema
	2.2 - Convert the tables to the new types
'''
import os

def get_csv_excel(folder_path: str):
	"""
	Return a list of csv files and excels in the folder passed
	:param folder_path: folder path to be searched
	:return: csv_list: list of the filepaths of csv's
			 excel_list: list of the filepaths of xls.* files
	"""
	csv_list = []
	excel_list = []
	for root, folders, filenames in os.walk(folder_path):
		for file in filenames:
			if file[-3:] == 'csv':
				csv_list.append(root + '/' +file)
			elif file.find('xls') >-1:
				excel_list.append(root + '/' +file)
	return csv_list,excel_list


