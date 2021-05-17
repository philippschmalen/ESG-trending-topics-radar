import yaml
import os
import pandas as pd
import logging

def load_config(filepath):
	"""Return dictionary with settings and final CSV path"""
	with open(filepath) as file:
		config = yaml.full_load(file)

		root_dir  = config['dir']['root'] # project root
		final_dir = config['dir']['final_data'] # final data dir from root
		filename = config['project']['analysis_file'] # filename to store

		path_analysis_file = os.path.join(root_dir, final_dir, filename+'.csv') 

		return config, path_analysis_file

def load_data(filepath):
	"""Read csv-only file from data_dir/filename"""
	logging.info(f"Load data from {filepath}")
	df = pd.read_csv(filepath)
	df = set_dtypes(df)

	return df


def set_dtypes(df):
    """ Set dtypes for columns """
    # drop rows where a column names appear (happened while appending to csv)
    df = df.loc[df[df.columns[0]] != df.columns[0]]
    # convert numerics
    df = df.apply(pd.to_numeric, errors='ignore')
    # parse query_timestamp
    df.query_timestamp = df.query_timestamp.apply(pd.to_datetime)

    df.reset_index(inplace=True, drop=True)

    return df