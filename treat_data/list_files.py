# What It does have to do!
'''
There is multiple files in csv and xlsx
1 - List all files
	1.1 - Select a specific path
	1.2 - If they are XLSX they have to converted do csv and append to paths
	1.3 - If they are csv add to lists
	1.4 - Else raise error
'''
import os

# return csv and excel from folder path
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


def repeated_filenames(list_file_paths):
	'''
	Receive a list of file_paths and return the files with the same name
	:param list_file_paths: list of file paths
	:return: the files that have the same names in the file path
	'''
	def filename_from_path(file_path):
		filename = file_path.split('/')[-1]
		return filename

	list_file_paths = sorted(list(map(lambda filename: filename_from_path(filename), list_file_paths)))
	list_file_paths = set([list_file_paths[index] for index in range(len(list_file_paths) - 1) if list_file_paths[index] == list_file_paths[index + 1]])
	return list_file_paths


def list_dup_files(files_list:list):
	'''
	Receive a file list and return the files that have repeated file name with path
	:param files_list:
	:return:
	'''
	dups_files = repeated_filenames(files_list)
	files = []
	for dup in dups_files:
		files.append([file_path for file_path in files_list if file_path.split('/')[-1] == dup])
	return files
