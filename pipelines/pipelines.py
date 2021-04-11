# general
import configparser
from datetime import timedelta, datetime
import os
import json
import yaml
# prefect
from prefect import task, Flow, Parameter
from prefect.schedules import IntervalSchedule
# custom
from esg_trending_topics import extract, transform, load, deploy
from analysis_dashboard import (extract as analysis_extract, 
								transform as analysis_transform)



# ~-- SOURCE DATA: GOOGLE TRENDS 
@task(max_retries=3, retry_delay=timedelta(seconds=40))
def extract_related_queries(kw_list):
	return extract.get_queries(kw_list)

@task
def transform_related_queries(response, geo, blacklist):
	df_raw = transform.create_response_df(response, geo)
	df = transform.clean_data(df_raw, blacklist=blacklist)
	return df

@task
def export(df, path):
	load.write_to_csv(df, filename=path)





# ~-- DASHBOARD DATA 
@task
def load_all_query_data(raw_data_dir, filename, blacklist):
	"""Loads data from previous queries """
	df_raw = analysis_extract.load_data(raw_data_dir=raw_data_dir, filename=filename)
	df = transform.clean_data(df_raw, blacklist=blacklist)
	return df

@task
def transform_for_statistics(df):
	"""Generate statistics for analysis in Streamlit dashboard """
	df = analysis_transform.dashboard_data(df=df)
	return df

@task
def export(df, path):
	load.write_to_csv(df=df, filename=path)





# ~-- TREEMAP PLOT 
@task(nout=2)
def transform_plot_data(df, to_uppercase, top_n):
	df_trend, df_top = transform.plot_data(df, 
		to_uppercase=to_uppercase, 
		top_n=top_n)
	return df_trend, df_top

@task
def web_deployment(df_trend, df_top, project_name, top_n): 
	figure = deploy.create_plot(df_trend, df_top)
	# deploy.deploy_plot(figure, filename=project_name)





def main():
	# ~----------------- CONFIG -----------------~
	with open('../settings.yml') as file:
		config = yaml.full_load(file)
		timestamp 	= datetime.now().strftime("%y%m%d_%H%M")	

		PROJECT 	   = config['project']['name']
		KW_LIST        = config['query']['kw_list']
		BLACKLIST      = config['query']['blacklist']
		TO_UPPERCASE   = config['query']['uppercase']
		GEO 		   = config['query']['geo']
		TOP_N 	 	   = config['query']['top_n']
		ROOT_DIR	   = '../'
		RAW_DIR        = os.path.join(ROOT_DIR, config['dir']['raw_data'])
		FINAL_DIR      = os.path.join(ROOT_DIR, config['dir']['final_data'])
		FILENAME_RAW   = config['project']['filename']
		FILENAME_ANALYSIS = config['project']['analysis_file']
		CSV_RAW        = f"{FILENAME_RAW}_{timestamp}.csv"
		CSV_ANALYSIS   = f"{FILENAME_ANALYSIS}.csv"
		RAW_DATA_LOC   = os.path.join(RAW_DIR, CSV_RAW)
		FINAL_DATA_LOC = os.path.join(FINAL_DIR, CSV_ANALYSIS)
	
	# ~----------------- FLOW -----------------~
	# ~-- daily schedule
	# schedule = IntervalSchedule(
	# 	start_date=datetime.utcnow() + timedelta(seconds=1),
	# 	interval=timedelta(days=1),
	# )

	with Flow("etl") as flow: # , schedule=schedule

		# ~-- parameter
		raw_data_dir = Parameter(name="raw_data_dir")
		raw_data_loc = Parameter(name="raw_data_loc")
		final_data_loc = Parameter(name="final_data_loc")
		raw_filename = Parameter(name="raw_filename")
		kw_list 	 = Parameter(name="kw_list")
		blacklist    = Parameter(name="blacklist")
		to_uppercase = Parameter(name="to_uppercase")
		geo 		 = Parameter(name="geo", default='global')
		top_n 		 = Parameter(name="top_n", default=35)
		project_name = Parameter(name="project_name") 

		# # -- SOURCE DATA
		response = extract_related_queries(kw_list)
		df = transform_related_queries(response, geo, blacklist)
		
		# # -- TREEMAP
		df_trend, df_top = transform_plot_data(df, to_uppercase=to_uppercase, top_n=top_n)
		export(df, raw_data_loc)
		web_deployment(df_trend, df_top, project_name, top_n)

		# -- STREAMLIT DASHBOARD
		df_raw = load_all_query_data(raw_data_dir, raw_filename, blacklist)
		df_analysis = transform_for_statistics(df_raw)
		export(df_analysis, final_data_loc)

	# ~----------------- RUN -----------------~
	flow.run(
		raw_data_dir = RAW_DIR,
		raw_data_loc=RAW_DATA_LOC, 
		final_data_loc=FINAL_DATA_LOC,
		raw_filename = FILENAME_RAW,
		kw_list=KW_LIST,
		blacklist=BLACKLIST,
		to_uppercase=TO_UPPERCASE, 
		top_n=TOP_N, 
		project_name=PROJECT
		)


if __name__ == "__main__":
    main()
