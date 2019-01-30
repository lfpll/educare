import xlrd
import os
import csv


# Transforming multiple excel files with multiple worksheets to csvs
def xlsx_to_csv(file_path: str,delete = False,index_row=5):
	'''
	Convert the sheets of a xlsx file to multiple files of csv and return the new filepaths in a list
	:param file_path: string parameter with the path of the file to be converted
	:param file_path: boolean parameter that removes file after converting
	:return: list with the names of the csv files
	'''
	# Open the csv file with sheet_name and writes the data from the excel sheet
	def write_to_csv(sheet, sheet_name, folder_path):
		new_filename = "{folder}/{sheet_name}_xlsx_conv.csv".format(folder=folder_path,sheet_name=sheet_name)

		with open(new_filename, "w", newline='') as csv_file:

			csv_writer = csv.writer(csv_file, delimiter='|')
			for row_index in range(0,sheet.nrows) :
				csv_writer.writerow(sheet.row_values(row_index))
				# Logic that removes rows not wanted
		return new_filename

	wb = xlrd.open_workbook(file_path)
	sheet_names = wb._sheet_names
	folder_path = '/'.join(file_path[::-1].split('/')[1:])[::-1]
	sheet_files = []

	for sheet_name in sheet_names:
		filename = write_to_csv(sheet=wb.sheet_by_name(sheet_name), sheet_name=sheet_name, folder_path=folder_path)
		sheet_files.append(filename)

	if delete:
		os.remove(file_path)
	return sheet_files


def find_header(file_path):
	'''
	Receives a file path csv and returns the index of the header
	:param file_path:
	:return:
	'''
	with open(file_path) as csv_file:
		length_header = 0
		for index, row in enumerate(csv.reader(csv_file, delimiter="|")):
			length_row =0
			if len(row[len(row)-1])>0:
				length_row = len(row)
			if length_row > length_header:
				length_header = length_row
				index_header = index
	return index_header

def find_table_type(file_path):
	with open(file_path) as csv_file:
		for row in csv.reader(csv_file,delimiter='|'):
			if len(list(filter(lambda row: row.find('\n') >-1,row))) >0:
				return 'type_break_line'
		return 'type_blank_line'

def type_blank_line(path,header_index,delimiter):
	'''

	:param path: path of the csv file
	:param header_index: index of the header of the csv
	:param delimiter: delimiter of the csv file
	:return:
	'''
	rewriten_rows = []
	with open(path,'r') as csv_file,open(path+'tmp','w',newline='') as csv_out_file:
		read_handle = csv.reader(csv_file,delimiter=delimiter)
		write_handle = csv.writer(csv_out_file,delimiter='|')
		[next(read_handle)for _ in range(header_index)]
		for row in read_handle:

			# This is a pattern found for ignoring on appending more data in rows of censo
			if (row[0] == '' or row[1] == ''):
				if any([len(cell) > 0 for cell in row[2:]]):
					# One liner that uses row and the past row as reference to rewriting
					write_handle.writerow([row_val if len(row_val)>0 else ref_row  for row_val,ref_row in zip(row,father_row)])
				else:
					continue
			elif row[0] == '' and row[1] == '':
				write_handle.writerow(row)
				father_row = row


# TODO Implement better row selection based on \n
def type_break_line(path,header_index,delimiter='|'):
	'''

	:param path: path of the csv file
	:param header_index: index of the header of the csv
	:param delimiter: delimiter of the csv file
	:return:
	'''

	with open(path) as csv_file,open(path+'tmp','w',newline='') as csv_out_file:
		read_handle = csv.reader(csv_file, delimiter=delimiter)
		write_handle = csv.writer(csv_out_file,delimiter='|')
		[next(read_handle)for _ in range(header_index)]
		for row in read_handle:
			if not (row[0] == '' or row[1] == ''):
				if row[5].find('\n') > -1:
					for cell in row[5].split('\n'):
						new_row = [cell for cell in row]
						new_row[5] = cell
						write_handle.writerow(new_row)
				else:
					write_handle.writerow(row)

		os.remove(path)
		os.rename(path+'tmp',path)


