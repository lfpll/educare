from treat_data.boolean_conversion import gen_distinct_rows,separate_booleans,type_not_boolean_column

#TODO implement efficient function
def generate_bigquery_schema(csv_path,eficient=False):
    distinct_sets_list,enum_headers = gen_distinct_rows(csv_path)
    bools_sets,not_bools_sets = separate_booleans(distinct_sets_list)
    # Transforming list into bigquery types
    not_bools_sets = [(index,type_not_boolean_column(row_set)) for index,row_set in not_bools_sets]
    bools_sets = [(index,'BOOLEAN') for index,row in bools_sets]
    bools_sets.extend(not_bools_sets)
    bools_sets.sort(key=lambda tup:tup[0])

    # generating the json bigquery schema
    bigq_schema = {}
    for header_tup,type_tup in zip(enum_headers,bools_sets):
        bigq_schema[header_tup[1]] = type_tup[1]
    return bigq_schema