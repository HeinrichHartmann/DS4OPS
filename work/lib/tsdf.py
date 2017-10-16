#
# Load & Store [T]ime [S]eries [D]ata [F]rames
# 

import pandas as pd

def store(df, location):
    df_2 = df.set_index((df.index.astype("uint64") / 1e9).astype("uint64"))
    df_2.to_csv(location, float_format="%.4f")
    
def load(location):
    df=pd.read_csv(location, index_col=0)
    return df.set_index(pd.to_datetime(df.index, unit='s'))
