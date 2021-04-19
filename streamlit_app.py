import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_utils.app_utilities import load_config, load_data
from pipelines.esg_trending_topics.transform import add_features, plot_data
from pipelines.esg_trending_topics.deploy import create_plot_rising
from datetime import datetime, tzinfo, date
import os

# ~------------- SETTINGS -------------~
config    = load_config(filepath = "./settings.yml")
ROOT_DIR  = config['dir']['root']
FINAL_DIR = config['dir']['final_data']
FILENAME  = config['project']['analysis_file']
CSV       = os.path.join(ROOT_DIR, FINAL_DIR, FILENAME+'.csv') 
TO_UPPERCASE = config['query']['uppercase']

# intuitive column names
rename_dict = {'query': 'Keyword', 
				"rank_t": "Rank",
				'rank_t-1': "Previous rank", 
				'keyword': 'Topic', 
				'value': 'Raw Google Trends value', 
				'query_date': 'Date', 
				'rank_absolute_change': 'Change in ranking', 
				'new_entry_t': 'New this period',
				'dropout_t+1': 'Dropout next period'}

# Use the full page instead of a narrow central column
st.set_page_config(layout='wide')
# ~-----------------------------------~

# -- load data
df = load_data(filepath=CSV).query("ranking=='rising'")
df = df.sort_values(by='query_date')
df.query_date = pd.to_datetime(df.query_date).dt.strftime('%d.%m.%Y')




# -- select date to inspect data 
# most recent 
date_most_recent = df.loc[df.t == df.t.max(),'query_date'].unique()[0]

# select date with slider
selected_date = st.sidebar.select_slider('Slide to select', 
	value=date_most_recent,
	options=df.query_date.unique().tolist())
df_selected = df.loc[df.query_date==selected_date]

# select keyword 
selected_keyword = st.sidebar.multiselect('Select keyword for analysis', 
	default=df_selected.loc[df_selected.rank_t == 1,'query'].to_list()[0],
	options=df_selected['query'].unique().tolist())

# -- treemap data and figure
df_treemap = plot_data(df_selected, to_uppercase=TO_UPPERCASE, top_n=1000)[0]
fig_treemap = create_plot_rising(df_treemap).update_layout(height=500, width=1200)

# -- timeline data and figure
if selected_keyword:
	df_timeline = df.loc[df['query'].isin(selected_keyword)]
	df_timeline.query_date = pd.to_datetime(df_timeline.query_date, format='%d.%m.%Y')
	df_timeline.sort_values(by=['query_date', 'query'], inplace=True)
	df_timeline['query_date_end'] = df_timeline.query_date.shift()
	# df_timeline['query_date_end'] = df_timeline.query_date + (df_timeline.query_date-df_timeline.query_date.shift())

	fig_timeline = px.timeline(df_timeline, x_start="query_date", x_end="query_date_end", y="rank_t", color='query')
	fig_timeline['layout']['yaxis']['autorange'] = "reversed"
	# TODO: label axes



# select simple columns, rename, sort by Rank and reset index
df_show = df_selected.loc[:,list(rename_dict.keys())]\
			.rename(mapper=rename_dict, axis=1)\
			.sort_values(by='Rank')\
			.reset_index(drop=True)


st.title("ESG trending topics")

f"""Selected: {selected_date}. Data last updated {date_most_recent}. 

### Data docs

* Rank: Rank measured by search volume (here: Raw Google Trends value)
* Previous rank: ranking at previous period
* Change in ranking: Rank change from previous to currently selected period. __Note:__ negative values indicate higher ranking

* Winners: Those with the highest rank change from previous to current period
* Loosers: Those with the highest negative rank change from previous to current period

---
"""


st.plotly_chart(fig_treemap)

# display ranking for selected date
st.write(
'## All data',
df_show,

"## Top-10 ranking",
df_show.sort_values(by='Rank').loc[:,['Keyword', 'Rank', 'Change in ranking']].head(10),
"## Winners - highest gain in rank", 
df_show.loc[:,['Keyword', 'Rank', 'Previous rank', 'Change in ranking']]\
			.sort_values(by='Change in ranking', ascending=True).iloc[:10].reset_index(drop=True), 
"## Loosers - highest loss in rank",
df_show.loc[:,['Keyword', 'Rank', 'Previous rank', 'Change in ranking']]\
			.sort_values(by='Change in ranking', ascending=False).iloc[:10].reset_index(drop=True), 
"## Newly listed",
df_show.loc[df_show['New this period'] == 1, ['Keyword', 'Topic','Rank']],


)
"## Keyword rank timeline"
st.plotly_chart(fig_timeline)

