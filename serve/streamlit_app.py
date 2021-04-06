import streamlit as st
import pandas as pd
import plotly.express as px
from utils.app_utilities import load_config, load_data
from datetime import datetime, tzinfo, date
import os

# -- load config
config = load_config(filepath = "../settings.yml")
ROOT_DIR = config['dir']['root']
FINAL_DIR = config['dir']['final_data']
FILENAME = config['project']['analysis_file']
CSV = os.path.join(ROOT_DIR, FINAL_DIR, FILENAME+'.csv') 

# -- load data
df = load_data(filepath=CSV).query("ranking=='rising'")
df.query_date = pd.to_datetime(df.query_date).dt.strftime('%d.%m.%Y')

# -- process data
t_most_recent = df.t.max() 
# most recent date
date_most_recent = df.loc[df.t==t_most_recent].query_date.unique()[0]


# -- SELECTIONS
# date selection
selected_date = st.sidebar.select_slider('Slide to select', 
	value=date_most_recent,
	options=df.query_date.unique().tolist(), )
df_selected_date = df.loc[df.query_date==date_most_recent]
	
st.title("ESG trending topics")
st.write(f"""Last updated on __{date_most_recent}__.
	\nSelected: {selected_date}
	This is a preliminary overview. Here are some key variables

	* rank_t: ranking at currently selected period (t)
	* rank_t-1: ranking at previous period (t-1)
	* rank_absolute_change: ranking change from previous (t-1) to current (t) period
	* Winners: Those with the highest rank change from previous to current period
	* Loosers: Those with the highest negative rank change from previous to current period
	""")

# display ranking for selected date
st.write("## Ranking",
	df_selected_date.sort_values(by='rank_t').loc[:,['query', 'rank_t', 'rank_absolute_change']].head(10),
	df_selected_date.sort_values(by='rank_t').loc[:,['query','rank_t']].reset_index(drop=True), 
	"## Winners ", 
	df_selected_date.loc[:,['query', 'rank_t', 'rank_t-1', 'rank_absolute_change']].sort_values(by='rank_absolute_change', ascending=False).iloc[:10].reset_index(drop=True), 
	"## Loosers",
	df_selected_date.loc[:,['query', 'rank_t', 'rank_t-1', 'rank_absolute_change']].sort_values(by='rank_absolute_change', ascending=True).iloc[:10].reset_index(drop=True), 
	"## Newly listed",
	df_selected_date.loc[df.new_entry_t == 1, ['query', 'keyword','rank_t']]
	)


# df.loc[df.query_date]