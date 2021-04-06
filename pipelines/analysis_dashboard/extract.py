"""
~-- EXTRACT
Loads the queried data from the raw data directory
"""

from glob import glob
import os
import pandas as pd

def load_data(raw_data_dir, filename):
    # merge all data from directory
    data_files = glob(f'{os.path.join(raw_data_dir, filename)}*')
    print(raw_data_dir, filename)
    df_list = [pd.read_csv(file) for file in data_files]
    df = pd.concat(df_list).reset_index(drop=True)
    
    return df
