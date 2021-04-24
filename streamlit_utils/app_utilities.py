import yaml
import os
import pandas as pd

def load_config(filepath):
	"""Return dictionary with settings and final CSV path"""
	with open(filepath) as file:
		config = yaml.full_load(file)

		root_dir  = config['dir']['root'] # project root
		final_dir = config['dir']['final_data'] # final data dir from root
		filename = config['project']['analysis_file'] # filename to store

		csv = os.path.join(root_dir, final_dir, filename+'.csv') 

		return config, csv

def load_data(filepath):
	"""Read csv-only file from data_dir/filename"""
	df = pd.read_csv(filepath)
	return df