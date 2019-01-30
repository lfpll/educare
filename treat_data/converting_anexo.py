from treat_data.csv_modelling import xlsx_to_csv
from itertools import chain
from treat_data.list_files import get_csv_excel
from treat_data.censo import rewrite_data_dictionarie
import re
excel_files = get_csv_excel('../files/')[1]

regexp = re.compile("ANEXO I\W")
excel_files = [excel_file for excel_file in excel_files if regexp.search(excel_file)]
list_files = list(chain.from_iterable([xlsx_to_csv(file_path) for file_path in excel_files]))
