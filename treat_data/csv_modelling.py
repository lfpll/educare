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

