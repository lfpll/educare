from treat_data.boolean_conversion import gen_distinct_rows,separate_booleans

def generate_bigquery_schema(csv_path,eficient=False):
    distinct_sets_list,enum_headers = gen_distinct_rows(csv_path)
    bools_sets,not_bools_sets = separate_booleans(distinct_sets_list)

    bools_sets.extend(not_bools_sets)
    bools_sets.sort(lambda tup:tup[0])