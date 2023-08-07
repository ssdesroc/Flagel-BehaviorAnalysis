from behavioranalysis import loop_over_days
import pandas as pd
import statistics

column_list = ['Subject', 'Day', 'Total Lever Presses', 'Total CS Mag. Entries', 'Total NCS Mag. Entries',
               'Prob. Lever Press', 'Prob. Mag. Entry', 'Lat. Lever Press', 'Lat. Mag. Entry', 'Response Bias',
               'Prob. Difference', 'Lat. Difference', 'PavCA Index']


def PavCA(loaded_file, i):
    """
    :param loaded_file: file output from operant box, split by subject
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    for index in range(len(loaded_file['L'])):
        if loaded_file['L'][index] >= 8:
            loaded_file['L'][index] = 8
    for index in range(len(loaded_file['N'])):
        if loaded_file['N'][index] >= 8:
            loaded_file['N'][index] = 8

    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), loaded_file['C'][1], loaded_file['D'][1],
                         loaded_file['E'][1],
                         ((len(loaded_file['K'][0:25])-(loaded_file['K'][0:25].count(0)))/len(loaded_file['K'][0:25])),
                         ((len(loaded_file['M'][0:25]) - (loaded_file['M'][0:25].count(0))) / len(loaded_file['M'][0:25])),
                         statistics.mean(loaded_file['L'][0:25]), statistics.mean(loaded_file['N'][0:25]),
                         ((loaded_file['C'][1]-loaded_file['D'][1])/(loaded_file['C'][1]+loaded_file['D'][1])),
                         (((len(loaded_file['K'][0:25])-(loaded_file['K'][0:25].count(0)))/len(loaded_file['K'][0:25]))-((len(loaded_file['M'][0:25]) - (loaded_file['M'][0:25].count(0))) / len(loaded_file['M'][0:25]))),
                         -(statistics.mean(loaded_file['L'][0:25])-statistics.mean(loaded_file['N'][0:25]))/8,
                         statistics.mean([((loaded_file['C'][1]-loaded_file['D'][1])/(loaded_file['C'][1]+loaded_file['D'][1])), (((len(loaded_file['K'][0:25])-(loaded_file['K'][0:25].count(0)))/len(loaded_file['K'][0:25]))-((len(loaded_file['M'][0:25]) - (loaded_file['M'][0:25].count(0))) / len(loaded_file['M'][0:25]))), -(statistics.mean(loaded_file['L'][0:25])-statistics.mean(loaded_file['N'][0:25]))/8])
                         ]],
                       columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, PavCA)
print(df.to_string())
df.to_excel("output.xlsx")