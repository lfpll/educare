import csv

file_path = r'/home/luizfernandolobo/PycharmProjects/educare/files/Censo Escolar/2017 (Atualizado em 02/DADOS/DOCENTES_NORTE.CSV'


# Return a list of sets with the unique values of each row in a csv
def gen_distinct_table(file_name):
	with open(file_name,'r') as file:
		reader = csv.reader(file,delimiter="|",quotechar='"')
		header = next(reader)
		list_unq= [set() for _ in list(range(0, len(header)))]
		for row in reader:
			[unq_set.add(row_val) for row_val,unq_set in zip(row, list_unq) if (row_val != '' and len(row_val)<2)]

		return  list_unq

# Receives a list of sets and enumerates.
# Return two lists separated by the ones that can be transformed to boolean and the ones that can't
def separate_booleans(rows_set):
	rows_set = list(enumerate(rows_set))
	less_than_two = [tup_ind for tup_ind in rows_set if len(tup_ind[1])<=2]
	not_binary = [tup_ind for tup_ind in rows_set if len(tup_ind[1])>2]
	return less_than_two, not_binary


# Receives a list of sets with length smaller then 3 enumerated
# Returns a list enumerated with dicts referencing the values received to True or False
def reference_to_boolean(enum_sets):
	convert_ref = []
	for index,row_set in enum_sets:
		if len(row_set) >0:
			row_set = iter(row_set)
			ref_dict = {next(row_set): True}
			next_val = next(row_set, False)
			if next_val:
				ref_dict[next_val] = False
			convert_ref.append((index,ref_dict))
	return convert_ref


def convert_table_to_bool(file_path, bool_set_reference):
	final_file = []
	with open(file_path, 'r') as in_file:
		reader = csv.reader(in_file,delimiter="|")
		final_file.append(next(reader))
		for row in reader:
			for index,bool_dict in bool_set_reference:
				if row[index] != '': row[index] = (bool_dict[row[index]])
			final_file.append(row)
	with open(file_path[:-4] + '_converted.csv', 'w') as out_file:
		writer = csv.writer(out_file, delimiter="|")
		[writer.writerow(row) for row in final_file]



distincts = gen_distinct_table(file_path)
binary,not_binary = separate_booleans(distincts)
to_bool = reference_to_boolean(binary)
convert_table_to_bool(file_path,to_bool)





