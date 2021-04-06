#!/bin/bash

# HOW TO UPLOAD A LOCAL FILE TO A LINUX SERVER

# general command
# pscp [options] [user@]host:[source target]
# replace 'user' with name of putty session (here it is by chance also the username)
pscp -pw Papasierra1 -r ./ cloudsigma:/home/cloudsigma/dev/esg_trends

# single files
pscp -pw Papasierra1 ./settings.yml cloudsigma:/home/cloudsigma/dev/esg_trends

# RUN PYTHON PROCESS IN BACKGROUND
nohup python script.py &

# check if process runs in background
ps -ef | grep python


# HOW TO: conda environment
# export 
	# conda env export --no-builds > environment.yml
# create environment form yml file on server (after upload)
	# conda env create -f environment.yml
# If you encounter error
	# ResolvePackageNotFound:
	#   - m2w64-gmp=6.1.0
	#   - m2w64-gcc-libs-core=5.3.0
# SOLUTION --> remove packages manually from yml

# list remote files
# pscp -ls -pw Papasierra1 cloudsigma:/home/cloudsigma/dev/esg_trends


