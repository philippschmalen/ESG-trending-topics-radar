
import pandas as pd
import os


def write_to_csv(df, filename):
    # file does not exist --> write header
    if not os.path.isfile(f'{filename}'):
        df.to_csv(f'{filename}', index=False)
    # file exists so append data without writing the header
    else:
        df.to_csv(f'{filename}', index=False, header=False, mode='a')
