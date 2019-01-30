import csv
from treat_data.list_files import list_dup_files,get_csv_excel

# def rewrite_csv_anexo(file_path:str,index_row:int=5):
# 	'''
# 	Receives a csv file with id and parameter on the first two collumns
# 	Split the data in the "index_row" for better vizualization
# 	:param file_path: path of the csv file
# 	:param index_row: row that has the data to be splitted
# 	:return: nothing
# 	'''
# 	list_final = []
# 	with open(file_path, newline='') as csv_file:
# 		csv_iter = csv.reader(csv_file, delimiter='|')
# 		for row in csv_iter:
# 			if len(row[0]) > 0 and len(row[1]) > 0:
# 				if row[5].find('\n') >-1:
# 					for value in row[index_row].split('\n'):
# 						new_row = list()
# 						new_row.extend(row)
# 						new_row[5] = value
# 						list_final.append(new_row)
# 				else:
# 					list_final.append(row)
#
# 	with open(file_path, 'w', newline='') as csv_file:
# 		csv_writer = csv.writer(csv_file, delimiter='|')
# 		for write_row in list_final:
# 			csv_writer.writerow(write_row)


def eval_data_dicts(ref_csv, comp_csv, separator='|', key_row_index=0,ignore_header = True):
	'''
	Compare two dicitonaries of data in csv and returns the keys that are different
	:param ref_csv: csv that is the reference
	:param comp_csv: csv that is to be compared as the reference
	:param separator: separator of the csv
	:return:
	'''

	with open(ref_csv) as csv_file:
		reader = csv.reader(csv_file,delimiter=separator)
		if ignore_header: next(reader)
		keys_ref = set([row[key_row_index] for row in reader])

	with open(comp_csv) as csv_file:
		reader = csv.reader(csv_file,delimiter=separator)
		if ignore_header: next(reader)
		keys_comp = set([row[key_row_index] for row in reader])

	not_in_comp = keys_ref - keys_comp
	not_in_ref = keys_comp - keys_ref

	return not_in_ref,not_in_comp

#TODO change with a better written solution
def compare_duplicates(file_list,replacer='_xlsx_conv.csv'):
	'''
	Function that compare dictionaries in csv files in the file oriented structure of this project
	returns the files that have differences from the last reference (current 2017)
	:param file_list: list of filepaths
	:param replacer: replace of the file_paths that can be removed
	:return: retun a dict with the differences between the years
	'''

	files_dup = list_dup_files(file_list)
	sheets = {}
	for file_list in files_dup:
		sheet_name = file_list[0].split('/')[-1].replace(replacer,'')
		duplicates = [{'year':dup.split('/')[3][:4],'path':dup} for dup in file_list]
		duplicates.sort(key= lambda obj:obj['year'], reverse=True)
		ref_dict = duplicates[1]
		comp_dicts = duplicates[1:]

		dict_years = dict()

		for comp in comp_dicts:
			not_in_ref,not_in_comp = eval_data_dicts(ref_dict['path'],comp['path'],key_row_index=1)
			for val in not_in_ref:
				if val in dict_years.keys():
					dict_years[val].append(comp['year'])
				else:
					dict_years[val] = [comp['year']]


		sheets[sheet_name] = dict_years
	return sheets


# csv_f,excel_f = get_csv_excel('../files/')
# csvs = [file for file in csv_f if file.find('ANEXO I/') > -1 or file.find('ANEXO I ') > -1]
# print(compare_duplicates(csvs))