
import pandas as pd
import os

def write_to_csv(df, filename):
	# if file does not exist write header 
	if not os.path.isfile(f'{filename}'):
		df.to_csv(f'{filename}', index=False) 
	else: # else it exists so append without writing the header
		df.to_csv(f'{filename}', index=False, mode='a') 


	
