import openpyxl
import csv


# Transforming multiple excel files with multiple worksheets to csvs
def inep_xlsx_csv_filter(file_path):

	# Open the csv file with sheet_name and writes the data from the excel sheet
	def write_to_csv(sheet, sheet_name, folder_path):
		with open(folder_path + '/' + sheet_name + '.csv', "w", newline='') as csv_file:
			csv_writer = csv.writer(csv_file, delimiter='|')
			for row in sheet.rows:
				row_write = list(map(lambda cell: cell.value, row))

				# Logic that removes rows not wanted
				if row_write[1] is not None and row_write[2] is not None:
					csv_writer.writerow(row_write)

	wb = openpyxl.load_workbook(file_path, read_only=True)
	sheet_names = wb.sheetnames
	folder_path = '/'.join(file_path[::-1].split('/')[1:])[::-1]
	for sheet_name in sheet_names:
		write_to_csv(sheet=wb[sheet_name], sheet_name=sheet_name, folder_path=folder_path)


# Re-writes separating the columns in multiple rows for each option
# For better handling to create a schema and transforming a 0-1 to bolean
def rewrite_csv(file_path):
	global docente

	list_final = []
	with open(file_path, newline='') as csv_file:
		docente = csv.reader(csv_file, delimiter='|')
		for row in docente:
			if row[5].find('\n') > -1:
				for reference in row[5].split('\n'):
					new_row = list()
					new_row.extend(row)
					new_row[5] = reference
					list_final.append(new_row)
			else:
				list_final.append(row)

	with open(file_path, 'w', newline='') as csv_file:
		docente = csv.writer(csv_file, delimiter='|')
		for row in list_final:
			docente.writerow(row)

file_path = r'/home/luizfernandolobo/PycharmProjects/download_zips/files/Censo Escolar/2017 (Atualizado em 02/ANEXOS/ANEXO I - Dicionário de Dados e Tabelas Auxiliares/Dicionário de Dados da Educaç╞o Básica 2017.xlsx'

inep_xlsx_csv_filter(file_path)
