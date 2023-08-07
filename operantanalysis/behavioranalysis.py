import statistics
import os
import glob
from tkinter import filedialog
from tkinter import *  # noqa
import pandas as pd
from .eventcodes import eventcodes_dictionary
from natsort import natsorted, ns

__all__ = ["loop_over_days", "load_file",
           "extract_info_from_file", "DNAMIC_extract_info_from_file",
           "DNAMIC_loop_over_days", "get_events_indices"]


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
        for file in sorted(glob.glob(file_pattern)):
            loaded_file = load_file(file)
            df2 = behavioral_test_function(loaded_file, i)
            df = df.append(df2, ignore_index=True)

    return days, df


def loop_over_days_lickometer(column_list, behavioral_test_function):
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
        for file in sorted(glob.glob(file_pattern)):
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

    group_identities = fields_dictionary['Group'].split('/')
    fields_dictionary['Group'] = group_identities.pop(0)

    for remaining in group_identities:
        if ':' in remaining:
            next_group = remaining.split(':')
            fields_dictionary[next_group[0]] = next_group[1]

    return fields_dictionary


def extract_info_from_file(dictionary_from_file, time_conversion):
    """
    :param dictionary_from_file: dictionary of all the fields and their values contained in the file (like subject, group, or w array)
    :param time_conversion: conversion number the timecode needs to be divided by to get seconds
    :return: timecode and eventcode lists derived from the w array
    """
    time_event_codes = dictionary_from_file["W"].split()

    for num in time_event_codes:
        if ':' in num:
            time_event_codes.remove(num)
    for num in time_event_codes:
        time_event_codes[time_event_codes.index(num)] = str(int(float(num)))

    timecode = []
    eventcode = []
    first_timecode = (float(time_event_codes[0][:-4]) / time_conversion)

    for num in time_event_codes:
        if num == time_event_codes[0]:
            timecode += [0.0]
        else:
            timecode += [round((float(num[:-4]) / time_conversion) - first_timecode, 2)]
        eventcode += [eventcodes_dictionary[int(num[-4:])]]

    return timecode, eventcode


def DNAMIC_loop_over_days(column_list, behavioral_test_function):
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
        for file in sorted(glob.glob(file_pattern)):
            (eventcode, timecode, fields_dictionary) = DNAMIC_extract_info_from_file(file)
            df2 = behavioral_test_function(eventcode, timecode, fields_dictionary, i)
            df = df.append(df2, ignore_index=True)

    return days, df


def DNAMIC_extract_info_from_file(filename):
    df = pd.read_csv(filename, sep=':', names=['event', 'timestamp'])
    df['timestamp'] = df['timestamp'].str.strip()

    # 0, 0, 0 appears after successful initialization --> serves as a cutoff mark

    end_of_init_idx = df.loc[df['timestamp'] == '0'].index[-1]
    body_start_idx = end_of_init_idx + 1

    keys = df[:body_start_idx]['event'].tolist()
    values = df[:body_start_idx]['timestamp'].tolist()
    fields_dictionary = dict(zip(keys, values))

    df_body = df[body_start_idx:-2]

    eventcode = df_body['event'].tolist()
    eventcode = [eventcodes_dictionary[int(i)] for i in eventcode]
    timecode = df_body['timestamp'].tolist()
    timecode = [int(i) / 1000 for i in timecode]

    return eventcode, timecode, fields_dictionary


def get_events_indices(eventcode, eventtypes):
    """
    :param eventcode: list of event codes from operant conditioning file
    :param eventtypes: list of event types to index
    :return: list of indices of target events
    """
    return [i for i, event in enumerate(eventcode) if event in eventtypes]

