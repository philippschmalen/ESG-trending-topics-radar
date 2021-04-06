
import pandas as pd

# ~------------------ LOAD ------------------~
def write_to_csv(df, filename):
	print(f'\nExport data, dimension: {df.shape} to\t{filename}\n')
	print(df.head(3).to_markdown())		
	df.to_csv(f'{filename}', index=False) 
