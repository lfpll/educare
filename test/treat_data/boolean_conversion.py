from treat_data.boolean_conversion import *
import json


file_path = r'/home/luizfernandolobo/PycharmProjects/educare/files/Censo Escolar/2017 (Atualizado em 02/DADOS/DOCENTES_NORTE.CSV'
print('Distincts Executed')

distincts, header = gen_distinct_rows(file_path)

print('Separated booleans Executed')
bool_list, not_bools = separate_booleans(distincts)
type_def = Define_type()
# Generate the enumarated schema list and sort
schema_list = [(index,'BOOLEAN') for index,value in bool_list]
schema_list.extend([(index,define_int_string(value)) for index, value in not_bools])
schema_list.sort(key=lambda tup: tup[0])

schema_json = [{'name': tup_header[1], 'type':tup_val[1]} for tup_header, tup_val in zip(header, schema_list)]

with open('schema.json', 'w') as file:
	json.dump(schema_json,file)

print('To bool')
to_bool = reference_to_boolean(bool_list)
print('Writing')
convert_table_to_bool(file_path,to_bool)

