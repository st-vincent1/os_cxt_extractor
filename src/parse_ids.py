import pandas as pd

"""
Parsing .ids file
Don't need atm but may be useful in the future
"""
df = pd.read_csv('datasets/OpenSubtitles.en-pl.ids_sample.txt', delimiter='	', header=None)
df.columns = ['Source file', 'Target file', 'Source ID', 'Target ID']

df = df.to_numpy()
NUM_COL_SRC_ID = 2
NUM_COL_TGT_ID = 3
for num_col in range(NUM_COL_SRC_ID, NUM_COL_TGT_ID+1):
    for num_row in range(len(df)):
        df[num_row][num_col] = [s for s in df[num_row][num_col].split()]
