import csv
import re
import os
import gcsfs


def convert_schema(schema: dict, conversion_pattern: dict, ref_schema: dict):
    """ Function that receiveis a JSON schema of big table
        Convert schema to the new keys
    Arguments:
        schema {dict} -- JSON bigquery Schema
        conversion_pattern {dict} -- Dict with the conversion
    Returns:
        {dict} -- Converted schema with dict
    """
    converted_schema = {}
    for schema_key, column_type in schema.items():
        if schema_key not in conversion_pattern:
            message = 'Invalid key {key} on the schema translation'.format(key=schema_key)
            raise KeyError(message)
        converted_key = conversion_pattern[schema_key]
        if ref_schema[converted_key] != column_type:
            message = 'Different data type for {schema_key} converted to {new_key}, {schema_type} expected {ref_type}' \
                .format(schema_key=schema_key, new_key=converted_key, schema_type=column_type,
                        ref_type=ref_schema[converted_key])
            raise ValueError(message)
        converted_schema[converted_key] = column_type
    return converted_schema


def change_headers(csv_input_path: str, conversion_pattern: dict,project:str,token='cloud'):
    """ Receive a iterable of a table format
        A conversion pattern dict to convert the header
        Gets the header and convert it
    Arguments:
        orig_table {Iterable} -- Iterable of a table
        conversion_pattern {dict} -- Dict with conversion
    Raises:
        Exception: Object is not iterable
    """
    pattern = re.compile('\.csv$',re.IGNORECASE)
    out_file_name = pattern.sub('_tmp.csv',csv_input_path)
    new_header = list()
    fs = gcsfs.GCSFileSystem(project=project,token=token)
    with fs.open(csv_input_path, 'r') as in_file:
        csv_in_file = csv.reader(in_file)

        header_list = next(csv_in_file)
        for header in header_list:
            if header not in conversion_pattern:
                raise KeyError('Value for {header} not found in conversion'.format(header=header))
            new_header.append(conversion_pattern[header])

        with open(out_file_name, 'w') as out_file:
            csv_out_file = csv.writer(out_file)
            csv_out_file.writerow(new_header)
            [csv_out_file.writerow(row) for row in csv_in_file]
    os.remove(csv_input_path)
    os.rename(out_file_name,csv_input_path)
    return csv_input_path


fsgcsfs.GCSFileSystem(project='my-google-project')