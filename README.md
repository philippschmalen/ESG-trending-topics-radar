# ESG trending topics

__Goal__ 
> Stay ahead of the curve in ESG and sustainable finance topics. Stay informed with a dashboard on what is trending on Google.

## Getting started

Create the conda virtual environment with 

```bash
conda env create -f environment.yml
```


### Folder structure
```bash
├───data
│   ├───0_external # store google trends data
│   ├───0_raw # source and immutable data
│   ├───1_interim # temporarily created data, e.g. for preprocessing
│   └───2_final # ready-to-use datasets
├───docs
│   ├───data_dictionaries
│   └───references
├───notebooks # exploration and code drafts
├───output
│   ├───features
│   ├───models
│   └───reports
│       └───figures
├───pipelines
│   ├───esg_trending_topics
│   └───tests
│       └───fixtures
└───serve
    └───tests
        └───fixtures
```

## Project Roadmap

1. Research: Where to get the data
    1. Google trends API capabilities?
    1. Google search API?
    1. Google keywords API?
    1. optional: Trending tweets
    1. optional: News headlines
1. Trial and error with notebooks
    1. collect data
    1. refactor to basic functions
    1. Exploration: Does the data answer the question?
1. Implement scripts
    1. create functions
    1. refactor
    1. tests: hypothesis, mockup, pandas.testing
    1. optional: prefect DAG
1. Visuals
    1. plotly
    1. dash
1. Documentation
    1. readme
    1. blog

## Prefect

The project relies on three main tasks: Data collection, preparation and  deployment. I use [Prefect](https://www.prefect.io/) to manage and execute these tasks and handle errors. The latter is crucial when we deal with any sort of queries that could fail. The Google Trends API sometimes returns errors due to rate limits, server timeout or an incorrect query which raises exceptions. Prefect not only manages them, but also allows me to build the project around tasks that easily modularize and can be exchanged. 

Beyond this, it enables me to think about further features I can add for the project. Suppose, I want to build other dashboards or even apps that take the same data input. All I have to add is another task that branches from the data collection step. Or I could extend the data collection and then create branches for each project feature. 

 <!-- TODO: add image of branches in prefect -->

## Discussion

### Possible extensions

#### Interactions

Add a clickable link which redirects you to Google and the keyword.  

#### Visually

Create large appealing tiles. 

Make tile background based on `keyword` with transparency for half pastel 
color and half photos. Photos can be a topic picture or abstract from pexels.

#### Data

Add more dimensions to be selected as tiles or dropdown menu. These could be region (`geo`) and platform specific like youtube (`gprop`). 

Other data sources are relevant as well, such as think tank publications or CEO addresses.   


1. Google search API
1. Google keywords API
1. Trending tweets
1. News headlines or articles
2. NGO reports or letters like the one from Larry Fink
3. official reports, such as Sustainable finance beirat


#### Query 

```python 
# get queries across geo and gprop
for geo in GEO:
    for gprop in GPROP:
#         build payload here
#         run query
#         store output

```




