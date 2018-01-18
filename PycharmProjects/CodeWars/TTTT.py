import pandas as pd
import numpy as np


path_to_skipped = "Z:\\Tetervak\\skipped_records_20180116_163000.xlsx"
path_to_file_stage = "Z:\\Tetervak\\File-stage_new.csv"

df_fs = pd.read_csv(path_to_file_stage, header=None, delimiter=';')


df_skipped = pd.read_excel(path_to_skipped, header=None)
for i in range(len(df_skipped[0])):
    df_skipped[0][i]=df_skipped[0][i].replace("'",'')


final = df_fs.loc[df_fs[0].isin(df_skipped[0])]


# df_skipped.set_index(0, inplace =True)
# final.set_index(0, inplace =True)


a = pd.merge(df_skipped, final, on=[0])

a = a[a['1_x']!=a['1_y']]

print(a)



