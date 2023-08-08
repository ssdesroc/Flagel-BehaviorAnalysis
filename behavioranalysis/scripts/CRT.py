from behavioranalysis import loop_over_days
import pandas as pd

column_list = ['Subject', 'Active Nosepokes', 'Inactive Nosepokes', 'Lever Presses', 'Incentive Value Index']


def CRT(loaded_file, i):
    """
    :param loaded_file: file output from operant box, split by subject
    :param i: number of days analyzing, user input
    :return: data frame of all analysis extracted from file (one animal)
    """

    act_np = loaded_file['D'][0]  # total active nosepokes
    inact_np = loaded_file['E'][0]  # total inactive nosepokes
    tot_lev = loaded_file['C'][0]  # total lever presses

    # Incentive Value Index = (active nosepokes + total lever presses)-inactive nosepokes
    IVI_Ind = (act_np+tot_lev)-inact_np

    df2 = pd.DataFrame([[loaded_file['Subject'], act_np, inact_np, tot_lev, IVI_Ind]], columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, CRT)
print(df.to_string())
df.to_excel("output.xlsx")
