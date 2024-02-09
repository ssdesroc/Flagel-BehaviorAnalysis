from behavioranalysis import loop_over_days
import pandas as pd
import statistics

column_list = ['Subject', 'Day', 'Small Total Lever Presses', 'Large Total Lever Presses',
               'Small CS Mag. Entries', 'Large CS Mag. Entries',
               'NCS Mag. Entries',
               'Small Prob. Lever Press', 'Large Prob. Lever Press',
               'Small Prob. Mag. Entry', 'Large Prob. Mag. Entry',
               'Small Lat. Lever Press', 'Large Lat. Lever Press',
               'Small Lat. Mag. Entry', 'Large Lat. Mag. Entry',
               'Small Response Bias', 'Large Response Bias',
               'Small Prob. Difference', 'Large Prob. Difference',
               'Small Lat. Difference', 'Large Lat. Difference',
               'Small PavCA Index', 'Large PavCA Index']


def PavCA(loaded_file, i):
    """
    :param loaded_file: file output from operant box, split by subject
    :param i: number of days analyzing, user input
    :return: data frame of all analysis extracted from file (one animal)
    """
    day = int(i + 1)  # day
    sm_tot_lev = loaded_file['C'][1]  # total lever presses
    lg_tot_lev = loaded_file['C'][2]  # total lever presses
    sm_tot_mag_CS = loaded_file['D'][1]  # total magazine entries during CS
    lg_tot_mag_CS = loaded_file['D'][2]  # total magazine entries during CS
    tot_mag_NCS = loaded_file['E'][1]  # total magazine entries during non-CS (ITI)
    # average probability of lever press on a trial (subtract 0 values from total trials/total trials)
    sm_prob_lev = ((len(loaded_file['K'][0:15]) - (loaded_file['K'][0:15].count(0))) / len(loaded_file['K'][0:15]))
    lg_prob_lev = ((len(loaded_file['K'][15:31]) - (loaded_file['K'][0:31].count(0))) / len(loaded_file['K'][0:31]))
    # average probability of magazine entry on a trial (subtract 0 values from total trials/total trials)
    sm_prob_mag = ((len(loaded_file['M'][0:15]) - (loaded_file['M'][0:15].count(0))) / len(loaded_file['M'][0:15]))
    lg_prob_mag = ((len(loaded_file['M'][15:31]) - (loaded_file['M'][15:31].count(0))) / len(loaded_file['M'][15:31]))
    sm_lat_lev = statistics.mean(loaded_file['L'][0:15])  # average latency to lever press during CS
    lg_lat_lev = statistics.mean(loaded_file['L'][15:31])  # average latency to lever press during CS
    sm_lat_mag = statistics.mean(loaded_file['N'][0:15])  # average latency to magazine entry during CS
    lg_lat_mag = statistics.mean(loaded_file['N'][15:31])  # average latency to magazine entry during CS

    sm_RSBias = (sm_tot_lev-sm_tot_mag_CS)/(sm_tot_lev+sm_tot_mag_CS)  # Response Bias = (tot_lev-tot_mag)/(tot_lev+tot_mag)
    lg_RSBias = (lg_tot_lev - lg_tot_mag_CS) / (lg_tot_lev + lg_tot_mag_CS)  # Response Bias = (tot_lev-tot_mag)/(tot_lev+tot_mag)
    sm_Prob_Diff = sm_prob_lev - sm_prob_mag  # difference between lever and magazine contact probabilities
    lg_Prob_Diff = lg_prob_lev - lg_prob_mag  # difference between lever and magazine contact probabilities
    sm_Lat_Diff = -(sm_lat_lev - sm_lat_mag)/8  # negative difference between lever and magazine latencies/cue length
    lg_Lat_Diff = -(lg_lat_lev - lg_lat_mag) / 8  # negative difference between lever and magazine latencies/cue length
    # PavCA Index = average of response bias, probability difference, and latency difference
    sm_PavCA_Ind = statistics.mean([sm_RSBias, sm_Prob_Diff, sm_Lat_Diff])
    lg_PavCA_Ind = statistics.mean([lg_RSBias, lg_Prob_Diff, lg_Lat_Diff])

    df2 = pd.DataFrame([[loaded_file['Subject'], day, sm_tot_lev, lg_tot_lev,
                         sm_tot_mag_CS, lg_tot_mag_CS,
                         tot_mag_NCS,
                         sm_prob_lev, lg_prob_lev,
                         sm_prob_mag, lg_prob_mag,
                         sm_lat_lev, lg_lat_lev,
                         sm_lat_mag, lg_lat_mag,
                         sm_RSBias, lg_RSBias,
                         sm_Prob_Diff, lg_Prob_Diff,
                         sm_Lat_Diff, lg_Lat_Diff,
                         sm_PavCA_Ind, lg_PavCA_Ind]], columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, PavCA)
print(df.to_string())
df.to_excel("output.xlsx")
