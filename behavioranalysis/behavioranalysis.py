import statistics
import os
import glob
from tkinter import filedialog
from tkinter import *  # noqa
import pandas as pd
from .eventcodes import eventcodes_dictionary
from natsort import natsorted, ns

__all__ = ["loop_over_days", "load_file"]


def loop_over_days(column_list, behavioral_test_function):
    """
    :param column_list: list of strings/column titles for analysis that will be output in a table
    :param behavioral_test_function: function that contains all the analysis functions to run on each file
    :return: one concatenated data table of analysis for each animal for each day specified
    """
    days = int(input("How many days would you like to analyze?"))
    df = pd.DataFrame(columns=column_list)

    for i in range(days):
        root = Tk()  # noqa
        root.withdraw()
        folder_selected = filedialog.askdirectory()
        file_pattern = os.path.join(folder_selected, '*')
        x = 0
        for file in sorted(glob.glob(file_pattern)):
            with open(file) as f:
                f_out = None
                for line in f:
                    if line.startswith('Start Date'):  # we need a new output file
                        x = x+1
                        if f_out:
                            f_out.close()
                        f_out = open(os.path.join(folder_selected, f'file{x}.txt'), 'w')
                    if f_out:
                        f_out.write(line)
                if f_out:
                    f_out.close()
        for file in sorted(glob.glob(file_pattern)):
            if 'txt' in file:
                loaded_file = load_file(file)
                df2 = behavioral_test_function(loaded_file, i)
                df = df.append(df2, ignore_index=True)

    return days, df


def load_file(filename):
    """
    :param filename: string that refers to single operant file location, file is txt
    :return: dictionary of all the fields and their values contained in the file (like subject, group, or w array)
    """
    with open(filename, "r") as fileref:
        filelines = fileref.readlines()

    fields_dictionary = {}

    for line in filelines:
        if line[0] != ' ' and line[0] != '\n':
            name = line.split(':')[0]
            fields_dictionary[name] = line.replace(name + ':', '')
            fields_dictionary[name] = fields_dictionary[name].replace('\n', '')
            fields_dictionary[name] = fields_dictionary[name].replace(' ', '')
        elif line[0] == ' ':
            fields_dictionary[name] += line
            fields_dictionary[name] = fields_dictionary[name].replace('\n', '')

    for key in fields_dictionary:
        if key == 'A' or key == 'B' or key == 'C' or key == 'D' or key == 'E' or key == 'F' or key == 'G' or key == 'H'\
                or key == 'I' or key == 'J' or key == 'K' or key == 'L' or key == 'M' or key == 'N' or key == 'O' \
                or key == 'P' or key == 'Q' or key == 'R' or key == 'S' or key == 'T' or key == 'U' or key == 'V' \
                or key == 'W' or key == 'X' or key == 'Y' or key == 'Z':

            list = fields_dictionary[key].split()

            for num in list:
                if ':' in num:
                    list.remove(num)
            for num in list:
                list[list.index(num)] = float(num)
            fields_dictionary[key] = list

    print(fields_dictionary)

    return fields_dictionary

