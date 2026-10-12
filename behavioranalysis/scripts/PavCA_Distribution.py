from behavioranalysis import loop_over_days
import pandas as pd
import statistics
import numpy as np

column_list = ['Subject', 'Day', 'Lev First', 'Mag First', 'Lev Only', 'Mag Only', 'None', 'Simultaneous']


def PavCA(loaded_file, i):
    """
    :param loaded_file: file output from operant box, split by subject
    :param i: number of days analyzing, user input
    :return: data frame of all analysis extracted from file (one animal)
    """
    day = int(i + 1)  # day
    levlat = loaded_file['L'][0:25]
    maglat = loaded_file['N'][0:25]
    mag_first = 0
    lev_first = 0
    mag_only = 0
    lev_only = 0
    none = 0
    both = 0

    # trials where lev vs. mag is first, only, or if no behavior happened for small and large trials
    for trial_number in range(len(levlat)):
        if (levlat[trial_number] < 8.000 and maglat[trial_number] < 8.000 and
                levlat[trial_number] > maglat[trial_number]):
            mag_first = mag_first + 1
        elif (maglat[trial_number] < 8.000 and levlat[trial_number] < 8.000 and
                maglat[trial_number] > levlat[trial_number]):
            lev_first = lev_first + 1
        elif maglat[trial_number] < 8.000 and levlat[trial_number] >= 8.000:
            mag_only = mag_only + 1
        elif maglat[trial_number] >= 8.000 and levlat[trial_number] < 8.000:
            lev_only = lev_only + 1
        elif maglat[trial_number] >= 8.000 and levlat[trial_number] >= 8.000:
            none = none + 1
        elif (maglat[trial_number] <= 8.000 and levlat[trial_number] <= 8.000 and
            maglat[trial_number] == levlat[trial_number]):
            both = both + 1

    df2 = pd.DataFrame([[loaded_file['Subject'], day, lev_first/len(levlat), mag_first/len(levlat),
                         lev_only/len(levlat), mag_only/len(levlat), none/len(levlat), both/len(levlat)
                         ]], columns=column_list)
    return df2


(days, df) = loop_over_days(column_list, PavCA)
print(df.to_string())
df.to_excel("output.xlsx")
