"""
~-- EXTRACT
Loads the queried data from the external data directory (data/0_external)
"""

from glob import glob
import os
import pandas as pd
import logging


def load_data(raw_data_dir, filename):
    # merge all data from directory
    data_files = glob(f'{os.path.join(raw_data_dir, filename)}*')
    logging.info(
        f"Load data from raw data dir: {raw_data_dir}, Filename: {filename}")
    # specify column dtypes
    df_list = [pd.read_csv(file) for file in data_files]
    df = pd.concat(df_list).reset_index(drop=True)
    df = set_dtypes(df)

    return df


def set_dtypes(df):
    """ Set dtypes for columns """
    # drop rows where a column names appear (happened while appending to csv)
    df = df.loc[df[df.columns[0]] != df.columns[0]]
    # convert numerics
    df = df.apply(pd.to_numeric, errors='ignore')
    # parse timestamps
    df.query_timestamp = df.query_timestamp.apply(pd.to_datetime)
    df.reset_index(inplace=True, drop=True)

    return df

# # TESTING ------------------------
# import streamlit as st

# import logging
# logging.basicConfig(level=logging.DEBUG)

# import sys
# sys.path.append('../')

# from esg_trending_topics.transform import clean_data
# from transform import dashboard_data, trends_statistics


# df_raw = load_data('../../data/0_external', filename='sustainable_finance')
# '', df_raw.dtypes

# st.stop()
# #############


# df = clean_data(df_raw, blacklist=['mykonos'])


# 'dataframe:', df, df.dtypes, df.shape, trends_statistics(df)


# # -------------------------------
