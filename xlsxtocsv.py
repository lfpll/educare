import openpyxl
import csv


def xlsx_to_csv(file_path):

	# Open the csv file with sheet_name and writes the data from the excel sheet
	def write_to_csv(sheet, sheet_name,folder_path):
		with open(folder_path+'/'+sheet_name+'.csv', "w", newline='') as csv_file:
			csv_writer = csv.writer(csv_file,delimiter='|')
			for row in sheet.rows:
				csv_writer.writerow(list(map(lambda cell: cell.value, row)))

	wb = openpyxl.load_workbook(file_path, read_only=True)
	sheet_names = wb.sheetnames
	folder_path = '/'.join(file_path[::-1].split('/')[1:])[::-1]
	for sheet_name in sheet_names:
		write_to_csv(sheet=wb[sheet_name],sheet_name=sheet_name,folder_path=folder_path)

xlsx_to_csv()
