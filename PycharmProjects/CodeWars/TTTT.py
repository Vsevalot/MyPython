import pandas as pd
import numpy as np
import mypyfunctions as myPy


path_to_skipped = "Z:\\Tetervak\\skipped_records_20180129_110000_sorted1.xlsx"
path_to_file_stage = "Z:\\Tetervak\\File-stage_AI.csv"

df_fs = pd.read_csv(path_to_file_stage, header=None, delimiter=';')

df_fs.drop(1, axis = 1, inplace = True)


df_skipped = pd.read_excel(path_to_skipped, header=None)





final = df_skipped.loc[df_skipped[0].isin(df_fs[0])]

final.drop(1, axis = 1, inplace = True)
final.drop(2, axis = 1, inplace = True)
final.drop(4, axis = 1, inplace = True)
final.drop(5, axis = 1, inplace = True)



final.to_csv('correction.csv', sep=';', encoding='utf-8')

f = myPy.readCSV('correction.csv')
f[-1] = [int(round(float(v))) for v in f[-1]]
myPy.write2csv(f, '1.csv')


#a = pd.merge(df_fs, final, on=[0])

#print(a)



