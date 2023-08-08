from behavioranalysis import loop_over_days
import pandas as pd
import statistics

column_list = ['Subject', 'Day', 'Total Lever Presses', 'Total CS Mag. Entries', 'Total NCS Mag. Entries',
               'Prob. Lever Press', 'Prob. Mag. Entry', 'Lat. Lever Press', 'Lat. Mag. Entry', 'Response Bias',
               'Prob. Difference', 'Lat. Difference', 'PavCA Index']


def PavCA(loaded_file, i):
    """
    :param loaded_file: file output from operant box, split by subject
    :param i: number of days analyzing, user input
    :return: data frame of all analysis extracted from file (one animal)
    """
    day = int(i + 1)  # day
    tot_lev = loaded_file['C'][1]  # total lever presses
    tot_mag_CS = loaded_file['D'][1]  # total magazine entries during CS
    tot_mag_NCS = loaded_file['E'][1]  # total magazine entries during non-CS (ITI)
    # average probability of lever press on a trial (subtract 0 values from total trials/total trials)
    prob_lev = ((len(loaded_file['K'][0:25]) - (loaded_file['K'][0:25].count(0))) / len(loaded_file['K'][0:25]))
    # average probability of magazine entry on a trial (subtract 0 values from total trials/total trials)
    prob_mag = ((len(loaded_file['M'][0:25]) - (loaded_file['M'][0:25].count(0))) / len(loaded_file['M'][0:25]))

    # transform latencies-->if over 8s (CS time) listed, then replace number with 8
    for index in range(len(loaded_file['L'])):
        if loaded_file['L'][index] >= 8:
            loaded_file['L'][index] = 8
    for index in range(len(loaded_file['N'])):
        if loaded_file['N'][index] >= 8:
            loaded_file['N'][index] = 8
    lat_lev = statistics.mean(loaded_file['L'][0:25])  # average latency to lever press during CS
    lat_mag = statistics.mean(loaded_file['N'][0:25])  # average latency to magazine entry during CS

    RSBias = (tot_lev-tot_mag_CS)/(tot_lev+tot_mag_CS)  # Response Bias = (tot_lev-tot_mag)/(tot_lev+tot_mag)
    Prob_Diff = prob_lev - prob_mag  # difference between lever and magazine contact probabilities
    Lat_Diff = -(lat_lev - lat_mag)/8  # negative difference between lever and magazine latencies/cue length
    # PavCA Index = average of response bias, probability difference, and latency difference
    PavCA_Ind = statistics.mean([RSBias, Prob_Diff, Lat_Diff])

    df2 = pd.DataFrame([[loaded_file['Subject'], day, tot_lev, tot_mag_CS, tot_mag_NCS, prob_lev, prob_mag, lat_lev,
                         lat_mag, RSBias, Prob_Diff, Lat_Diff, PavCA_Ind]], columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, PavCA)
print(df.to_string())
df.to_excel("output.xlsx")
