import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_utils.app_utilities import load_config, load_data
from pipelines.esg_trending_topics.transform import add_features, plot_data
from pipelines.esg_trending_topics.deploy import create_plot_rising
from datetime import datetime, tzinfo, date
import os

# Use the full page instead of a narrow central column
st.set_page_config(layout='wide')



# ~------------- CONFIG -------------~
config, analysis_csv = load_config(filepath = "./settings.yml")
to_uppercase = config['query']['uppercase']
intuitive_colnames = config['app']['rename']
# ~-----------------------------------~

# -- load data
df = load_data(filepath=analysis_csv).query("ranking=='rising'")
df = df.sort_values(by='query_date')
df.query_date = pd.to_datetime(df.query_date).dt.strftime('%d.%m.%Y')


# -- select date to inspect data 
date_select_recent = df.loc[df.t == df.t.max(),'query_date'].unique()[0] # most recent 

# select date with slider
selected_date = st.sidebar.select_slider('Slide to select', 
	value=date_select_recent,
	options=df.query_date.unique().tolist())
df_selected = df.loc[df.query_date==selected_date]

# select keyword 
selected_keyword = st.sidebar.multiselect('Select keyword for analysis', 
	default=df_selected.loc[df_selected.rank_t == 1,'query'].to_list()[0],
	options=df_selected['query'].unique().tolist())

# -- treemap data and figure
df_treemap = plot_data(df_selected, to_uppercase=to_uppercase, top_n=1000)[0]
'', df_selected
'', plot_data
fig_treemap = create_plot_rising(df_treemap).update_layout(height=500, width=1200)

# -- timeline data and figure
if selected_keyword:
	# subset data
	df_timeline = df.loc[df['query'].isin(selected_keyword)]
	# change date format
	df_timeline.query_date = pd.to_datetime(df_timeline.query_date, format='%d.%m.%Y')
	# sort by date
	df_timeline.sort_values(by=['query_date', 'query'], inplace=True)
	df_timeline['query_date_end'] = df_timeline.query_date.shift()

	# plot
	fig_timeline = px.timeline(df_timeline, x_start="query_date", x_end="query_date_end", y="rank_t", color='query')
	fig_timeline['layout']['yaxis']['autorange'] = "reversed"
	# TODO: label axes



# select simple columns, rename, sort by Rank and reset index
df_show = df_selected.loc[:,list(intuitive_colnames.keys())]\
			.rename(mapper=intuitive_colnames, axis=1)\
			.sort_values(by='Rank')\
			.reset_index(drop=True)
# make change in ranking intuitivef
df_show['Change in ranking'] = df_show['Change in ranking'].apply(lambda x: x*(-1))

df_win = df_show.loc[:,['Keyword', 'Rank', 'Previous rank', 'Change in ranking']]\
			.sort_values(by='Change in ranking', ascending=False).iloc[:10]\
			.reset_index(drop=True)
df_loose = df_show.loc[:,['Keyword', 'Rank', 'Previous rank', 'Change in ranking']]\
			.sort_values(by='Change in ranking', ascending=True).iloc[:10]\
			.reset_index(drop=True)
df_new = df_show.loc[df_show['New this period'] == 1, ['Keyword', 'Topic','Rank']]


st.title("ESG trending topics")

f"""Selected: {selected_date}. Data last updated {date_select_recent}. 

### Data docs

* Rank: Rank measured by search volume (here: Raw Google Trends value)
* Previous rank: ranking at previous period
* Change in ranking: Rank change from previous to currently selected period. 
__Note:__ Positive values indicate higher ranking in the previous period

* Winners: Those who gained the most from previous to current period
* Loosers: Those who lost the most rankings from previous to current period

---
"""


st.plotly_chart(fig_treemap)

'## Raw data'
with st.beta_expander("Raw data"): '', df_show
with st.beta_expander("Winners - Highest rank gains "): '', df_win
with st.beta_expander("Loosers - Highest rank losses "): '', df_loose
with st.beta_expander("Newly listed"): '', df_new

"## Ranking timeline"
st.plotly_chart(fig_timeline)

