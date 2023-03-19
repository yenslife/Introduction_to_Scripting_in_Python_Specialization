"""
Project for Week 3 of "Python Data Analysis".
Read and write CSV files using a dictionary of dictionaries.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv

def read_csv_fieldnames(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Ouput:
      A list of strings corresponding to the field names in
      the given CSV file.
    """
    out_list = []
    with open(filename, "r", encoding="UTF-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=separator, quotechar=quote)
        print(reader)
        for string in reader:
            print()
            for item in string:
                out_list.append(item)
            break

    return out_list


def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a list of dictionaries where each item in the list
      corresponds to a row in the CSV file.  The dictionaries in the
      list map the field names to the field values for that row.
    """
    out_list = []
    with open(filename, "r", encoding="UTF-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in reader:
            out_list.append(row)
    return out_list


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    out_dict = {}
    with open(filename, "r", encoding="UTF-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in reader:
            out_dict[row[keyfield]] = row
    return out_dict


def write_csv_from_list_dict(filename, table, fieldnames, separator, quote):
    """
    Inputs:
      filename   - name of CSV file
      table      - list of dictionaries containing the table to write
      fieldnames - list of strings corresponding to the field names in order
      separator  - character that separates fields
      quote      - character used to optionally quote fields
    Output:
      Writes the table to a CSV file with the name filename, using the
      given fieldnames.  The CSV file should use the given separator and
      quote characters.  All non-numeric fields will be quoted.
    """
    with open(filename, "w", encoding="UTF-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=separator, quotechar=quote, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for row in table:
            print(row)
            writer.writerow(row)


# for i in read_csv_as_list_dict("hightemp.csv", ",", ","):
#     print(i)
# print("=========")
# for i in read_csv_as_nested_dict("hightemp.csv", "Feb", ",", ","):
#     print(i)
# print("=========")
# print(read_csv_as_nested_dict("hightemp.csv", "Feb", ",", ","))
# print(read_csv_fieldnames("hightemp.csv", ",", ","))
# my_dic = {1:'a', 2:'b', 3:'c'}
# for i in my_dic:
#     print(i.value())
write_csv_from_list_dict("hightemp.csv", read_csv_as_list_dict("out.csv", ",", "\""), read_csv_fieldnames("out.csv", ",", "\""), ",", " ")
# write_csv_from_list_dict('hightemp.csv', [{'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14}, {'a': 20, 'b': 21, 'c': 22, 'd': 23, 'e': 24}, {'a': 30, 'b': 31, 'c': 32, 'd': 33, 'e': 34}, {'a': 40, 'b': 41, 'c': 42, 'd': 43, 'e': 44}], ['a', 'b', 'c', 'd', 'e'], ',', '"')