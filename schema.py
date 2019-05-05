import csv
import sys
import re
import json
import os
import gcsfs

# Class that define a file type of a string for generating DB's schema
class Define_type:
    def __init__(self, min_year: int = 1900):
        """
        Class to define a type to string

        Keyword Arguments:
                min_year {int} -- Minimun year of data regexp (default: {1900})
        """
        date_string = "^([3][0-1]|[0-2][0-9])/([1][0-2]|0?[1-9])/[%s-2019]$" \
            % str(min_year)
        self.date_regex = re.compile(date_string)
        self.int_regex = re.compile("^[0-9]+$")
        self.float_regex = re.compile(r"^([0-9]+)?\.[0-9]+$")
        self.bool_regex = re.compile("^TRUE|FALSE$")
        self.assigned_val = {2: 'INTEGER', 3: 'FLOAT',
                             4: 'DATETIME', 1: 'BOOLEAN', 5: 'STRING'}
    # Function that receives a string and define the type

    def classify_row(self, row_val: str):
        """ 
        Function to classify a string as a datatype

        Arguments:
                string {[str]} -- string to be classified

        Returns:
                [type] -- [description]
        """
        if isinstance(row_val, int) or (isinstance(row_val, str) and
                                        self.int_regex.search(row_val)):
            return 2
        elif isinstance(row_val, float) or (isinstance(row_val, str) and
                                            self.float_regex.search(row_val)):
            return 3
        elif isinstance(row_val, str) and self.date_regex.search(row_val):
            return 4
        elif isinstance(row_val, bool) or (isinstance(row_val, str) and
                                           self.bool_regex.search(row_val)):
            return 1
        elif isinstance(row_val, str):
            return 5
        else:
            raise Exception("Wans't able to define %s." % row_val)


def treat_dataframe(csv_file_path: str, delimiter: str = '|'):
    """

    Arguments:
            csv_file_path {str} -- the path file of the CSV

    Keyword Arguments:
            delimiter {str} -- delimiter of the csv file (default: {'|'})
    """
    with open(csv_file_path, 'r') as csv_file_in:
        csv_in = csv.DictReader(csv_file_in, delimiter=delimiter)
        header = next(csv_in)
        with open(csv_file_path.replace('.csv', '_tmp.csv'), 'w') as file_out:
            csv_out = csv.DictWriter(
                file_out, delimiter=delimiter, fieldnames=header)
            # add method to replace values
            [csv_out.writerow(next(csv_in)) for _ in csv_in]
        return csv_file_path

# Generate distinct values of each column for csv file


def gen_distinct_rows(csv_file_path: str, project:str, token:str='cloud'):
    """
    Generate list of sets with distinct values of each column

    Arguments:
            csv_file_path {[str]} -- path of the csv_file

    Returns:
            list_unq [list] -- sets with unique values of the CSV columns
            header [list] -- enumerated header of CSV
    """
    fs = gcsfs.GCSFileSystem(project=project, token=token)
    with fs.open(csv_file_path, 'r') as file:
        reader = csv.reader(file, delimiter="|", quotechar='"')
        header = next(reader)
        list_unq = [set() for _ in list(range(0, len(header)))]
        for row in reader:
            [unq_set.add(row_val)
                for row_val, unq_set in zip(row, list_unq) if (row_val != '')]
        return list_unq, enumerate(header)


# Function that separate booleans and non booleans from a list of columns
def separate_booleans(rows_set: list):
    """

    Receives a list with the  unique values for each column, separate into two lists for booleans and not booleans
    Arguments:
            rows_set {list} -- list of sets for with the values of the columns

    Returns:
            valid_bool [list] -- list with the boolean columns
            not_valid [list] -- list with not booleans columns
    """
    rows_set = list(enumerate(rows_set))
    valid_bool = []
    not_valid = []
    for tup_ind in rows_set:
        set_val = tup_ind[1]
        if all([(isinstance(val, int) and (val == 0 or val == 1)) or isinstance(val, bool) or (isinstance(val, str) and (val.lower() == 'true' or val.lower() == 'false' or val == '0' or val == '1')) for val in set_val]):
            valid_bool.append(tup_ind)
        else:
            not_valid.append(tup_ind)
    return valid_bool, not_valid


# Generate list with the types
def gen_column_types(columns_sets: list):
    """
    Generate a list of indexes with the column types 

    Arguments:
            columns_sets {list} -- unique values of columns
    Returns:
            row_types {list} -- return the indexed rows with the values
    """
    row_types = []
    type_class = Define_type()
    for index, column_set in columns_sets:
        type_list = map(type_class.classify_row, column_set)
        row_types.append((index, type_class.assigned_val[max(type_list)]))

    return row_types


def classify_csv(csv_path: str):
    """ Function that gets a CSV file path
        And generate a JSON bigtable schema
    
    Arguments:
        csv_path {[str]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    if not os.path.isfile(csv_path):
        raise Exception('File does not exists')
    try:
        # Receives the treated CSV removing junk white space
        treated_csv = treat_dataframe(csv_path)

        # Generate the list of uniques for each row
        list_sets, indexed_header = gen_distinct_rows(treated_csv)
        indexed_header = list(indexed_header)
        json_schema = {}

        # Separate the booleans and non booleans columns
        columns_bools, columns_no_bools = separate_booleans(rows_set=list_sets)

        # Define the types of the non boolean columns
        columns_types = gen_column_types(columns_sets=columns_no_bools)

        # Generating a list with the header and the variable type of the column
        tup_type = list(map(lambda column_tup: (
            indexed_header[column_tup[0]][1], column_tup[1]), columns_types))
        tup_bool_type = list(map(lambda bool_type: (
            indexed_header[bool_type[0]][1], 'BOOLEAN'), columns_bools))
        tup_type.extend(tup_bool_type)

        # Transforming the tuples into the json format for using as schema
        for header, column_type in tup_type:
            json_schema[header] = column_type
        return json_schema
    except Exception as e:
        raise e


if __name__ == "__main__":
    json_resp = classify_csv(sys.argv[1])
    json.dump(obj=json_resp, fp=open(sys.argv[2], 'w'))
