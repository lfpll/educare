from treat_data.list_files import repeated_filenames,list_dup_files
from treat_data.censo import eval_data_dicts
from treat_data.csv_modelling import find_header,find_table_type,type_break_line
import itertools
import csv
files_list =["./files/Censo Escolar/2012/2012/ANEXOS/ANEXO I/Tabela de Escola_xlsx_conv.csv" /
"./files/Censo Escolar/2012/2012/ANEXOS/ANEXO I/Tabela de Turma_xlsx_conv.csv",
"./files/Censo Escolar/2012/2012/ANEXOS/ANEXO I/Tabela de Matrícula_xlsx_conv.csv",
"./files/Censo Escolar/2012/2012/ANEXOS/ANEXO I/Tabela de Docente_xlsx_conv.csv",
"./files/Censo Escolar/2011/2011/ANEXOS/ANEXO I/Tabela de Escola_xlsx_conv.csv",
"./files/Censo Escolar/2011/2011/ANEXOS/ANEXO I/Tabela de Turma_xlsx_conv.csv",
"./files/Censo Escolar/2011/2011/ANEXOS/ANEXO I/Tabela de Matrícula_xlsx_conv.csv",
"./files/Censo Escolar/2011/2011/ANEXOS/ANEXO I/Tabela de Docente_xlsx_conv.csv",
"./files/Censo Escolar/2015/2015/ANEXOS/ANEXO I/Tabela de Escola_xlsx_conv.csv",
"./files/Censo Escolar/2015/2015/ANEXOS/ANEXO I/Tabela de Turma_xlsx_conv.csv",
"./files/Censo Escolar/2015/2015/ANEXOS/ANEXO I/Tabela de Matrícula_xlsx_conv.csv",
"./files/Censo Escolar/2015/2015/ANEXOS/ANEXO I/Tabela de Docente_xlsx_conv.csv",
"./files/Censo Escolar/2015/ANEXOS/ANEXO I/Tabela de Escola_xlsx_conv.csv",
"./files/Censo Escolar/2015/ANEXOS/ANEXO I/Tabela de Turma_xlsx_conv.csv",
"./files/Censo Escolar/2015/ANEXOS/ANEXO I/Tabela de Matrícula_xlsx_conv.csv",
"./files/Censo Escolar/2015/ANEXOS/ANEXO I/Tabela de Docente_xlsx_conv.csv",
"./files/Censo Escolar/2014/2014/ANEXOS/ANEXO I/Tabela de Escola_xlsx_conv.csv",
"./files/Censo Escolar/2014/2014/ANEXOS/ANEXO I/Tabela de Turma_xlsx_conv.csv",
"./files/Censo Escolar/2014/2014/ANEXOS/ANEXO I/Tabela de Matrícula_xlsx_conv.csv",
"./files/Censo Escolar/2014/2014/ANEXOS/ANEXO I/Tabela de Docente_xlsx_conv.csv",
"./files/Censo Escolar/2014/ANEXOS/ANEXO I/Tabela de Escola_xlsx_conv.csv",
"./files/Censo Escolar/2014/ANEXOS/ANEXO I/Tabela de Turma_xlsx_conv.csv",
"./files/Censo Escolar/2014/ANEXOS/ANEXO I/Tabela de Matrícula_xlsx_conv.csv",
"./files/Censo Escolar/2014/ANEXOS/ANEXO I/Tabela de Docente_xlsx_conv.csv",
"./files/Censo Escolar/2007/2007/ANEXOS/ANEXO I/Tabela de Escola_xlsx_conv.csv",
"./files/Censo Escolar/2007/2007/ANEXOS/ANEXO I/Tabela de Turma_xlsx_conv.csv",
"./files/Censo Escolar/2007/2007/ANEXOS/ANEXO I/Tabela de Matrícula_xlsx_conv.csv",
"./files/Censo Escolar/2007/2007/ANEXOS/ANEXO I/Tabela de Docente_xlsx_conv.csv",
"./files/Censo Escolar/2010/2010/ANEXOS/ANEXO I/Tabela de Escola_xlsx_conv.csv",
"./files/Censo Escolar/2010/2010/ANEXOS/ANEXO I/Tabela de Turma_xlsx_conv.csv",
"./files/Censo Escolar/2010/2010/ANEXOS/ANEXO I/Tabela de Matrícula_xlsx_conv.csv",
"./files/Censo Escolar/2010/2010/ANEXOS/ANEXO I/Tabela de Docente_xlsx_conv.csv",
"./files/Censo Escolar/2009/2009/ANEXOS/ANEXO I/Tabela de Escola_xlsx_conv.csv",
"./files/Censo Escolar/2009/2009/ANEXOS/ANEXO I/Tabela de Turma_xlsx_conv.csv",
"./files/Censo Escolar/2009/2009/ANEXOS/ANEXO I/Tabela de Matrícula_xlsx_conv.csv",
"./files/Censo Escolar/2009/2009/ANEXOS/ANEXO I/Tabela de Docente_xlsx_conv.csv",
"./files/Censo Escolar/2013/2013/ANEXOS/ANEXO I/Tabela de Escola_xlsx_conv.csv",
"./files/Censo Escolar/2013/2013/ANEXOS/ANEXO I/Tabela de Turma_xlsx_conv.csv",
"./files/Censo Escolar/2013/2013/ANEXOS/ANEXO I/Tabela de Matrícula_xlsx_conv.csv",
"./files/Censo Escolar/2013/2013/ANEXOS/ANEXO I/Tabela de Docente_xlsx_conv.csv",
"./files/Censo Escolar/2016/ANEXOS/ANEXO I/Tabela de Escola_xlsx_conv.csv",
"./files/Censo Escolar/2016/ANEXOS/ANEXO I/Tabela de Turma_xlsx_conv.csv",
"./files/Censo Escolar/2016/ANEXOS/ANEXO I/Tabela de Matrícula_xlsx_conv.csv",
"./files/Censo Escolar/2016/ANEXOS/ANEXO I/Tabela de Docente_xlsx_conv.csv",
"./files/Censo Escolar/2016/micro_censo_escolar_2016/ANEXOS/ANEXO I/Tabela de Escola_xlsx_conv.csv",
"./files/Censo Escolar/2016/micro_censo_escolar_2016/ANEXOS/ANEXO I/Tabela de Turma_xlsx_conv.csv",
"./files/Censo Escolar/2016/micro_censo_escolar_2016/ANEXOS/ANEXO I/Tabela de Matrícula_xlsx_conv.csv",
"./files/Censo Escolar/2016/micro_censo_escolar_2016/ANEXOS/ANEXO I/Tabela de Docente_xlsx_conv.csv",
"./files/Censo Escolar/2017 (Atualizado em 02/ANEXOS/ANEXO I - Dicionário de Dados e Tabelas Auxiliares/Anexo1 - Língua Indígena_xlsx_conv.csv",
"./files/Censo Escolar/2017 (Atualizado em 02/ANEXOS/ANEXO I - Dicionário de Dados e Tabelas Auxiliares/Anexo2 - Cursos Educ. Prof._xlsx_conv.csv"]


def check_repeated_files(list_files = files_list):
	'''
	Just praticting tome TOD
	:param list_files: list of files to be tested
	:return: none
	'''
	response = ["Tabela de Escola_xlsx_conv.csv",
	 "Tabela de Turma_xlsx_conv.csv",
	 "Tabela de Matrícula_xlsx_conv.csv",
	 "Tabela de Docente_xlsx_conv.csv"]
	filenames = repeated_filenames(list_files)
	assert set(response) == filenames


def check_eval_data_dicts(ref_csv='./ref.csv', comp_csv='./comp.csv'):
	'''
	Receive two lists
	:param ref_csv: reference csv file
	:param comp_csv: comparison csv file
	'''
	ref_not_in = {'header2'}
	comp_not_in = {'header45'}
	not_ref,nt_sm_resp = eval_data_dicts(ref_csv, comp_csv)
	assert ref_not_in == not_ref
	assert  comp_not_in == nt_sm_resp


def check_gen_list_dup(list_files = files_list):
	paths_interested = list_dup_files(list_files)
	result = files_list[:-2]
	result.sort()
	paths_interested = sorted(list(itertools.chain.from_iterable(paths_interested)))
	assert result == paths_interested

def check_find_header(file_path='../../files/Censo Escolar/2007/2007/ANEXOS/ANEXO I/Tabela de Docente_xlsx_conv.csv'):
	header_index = find_header(file_path)
	assert 1 == header_index

def check_find_table_type(file_path_type_1='../../files/Censo Escolar/2007/2007/ANEXOS/ANEXO I/Tabela de Docente_xlsx_conv.csv',file_path_type_2='../../files/Censo Escolar/2017 (Atualizado em 02/ANEXOS/ANEXO I - Dicionário de Dados e Tabelas Auxiliares/Tabela de Docente_xlsx_conv.csv'):
	assert 'type_blank_line' == find_table_type(file_path_type_1)
	assert 'type_break_line' == find_table_type(file_path_type_2)

def check_type_break_line(file_path,header_index,delimiter):
	with open(file_path,'r') as csvfile:
		reader_handle = csv.reader(csvfile,delimiter=delimiter)
		[next(reader_handle) for _ in range(header_index)]
		count_rows = 0
		for row in reader_handle:
			if row[5].find("\n") > -1:
				for cell in  row[5].split('\n'):
					count_rows += 1
			else:
				count_rows += 1
		assert len(type_break_line(path=file_path,header_index=header_index,delimiter=delimiter))  == count_rows
