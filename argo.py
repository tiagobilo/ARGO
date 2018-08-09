###Primary functions
def download_update_yomaha(savepath):
	"""
	Input: Folder where to save the dataset
	"""

	# Dependencies
	import warnings
	warnings.filterwarnings('ignore')

	import os
	import urllib
	import gzip


	## URLs of the Yomaha dataset and metadata
	url = ['http://apdrc.soest.hawaii.edu/projects/Argo/data/trjctry/0-Near-Real_Time/0-date_time.txt',
		'http://apdrc.soest.hawaii.edu/projects/Argo/data/trjctry/0-Near-Real_Time/WMO2DAC2type.txt',
		'http://apdrc.soest.hawaii.edu/projects/Argo/data/trjctry/0-Near-Real_Time/end-prog.lst',
		'http://apdrc.soest.hawaii.edu/projects/Argo/data/trjctry/0-Near-Real_Time/yomaha07.dat.gz']

	## Data Path
	path = os.path.expanduser(savepath)

	## Download the different metadata files
	for i in xrange(len(url)-1):
		print('Downloading: ' + str(url[i]))

		response = urllib.urlopen(url[i])
		outfile = path+url[i][74:]


		print('Saving: ' + outfile)
	
		with open(outfile, 'wb') as outfile:
			outfile.write(response.read())


	## Downloading compressed dataset 
	print('Downloading: ' + str(url[-1]))

	response = urllib.urlopen(url[-1])
	compressed_file = response.read()

	filename = path + url[-1][74:]

	print('Saving: ' + filename)
	with open(filename, 'wb') as outfile:
		outfile.write(compressed_file)


	## Decompressing dataset file
	print('Decompressing: ' + filename)

	with gzip.open(filename, 'rb') as content:
		content = content.read()


	filename = path + url[-1][74:-3]

	with open(filename, 'wb') as outfile:
		outfile.write(content)

	## Print database last update
	with open(path + url[0][74:]) as infile:
		print('\n Last Update: ' + infile.read())



def read_yomaha(filename):
	"""
	Input: YoMaHa dataset .dat path+filename
	
	Returns: Pandas dataframe with the individual
	trajectories of ARGO floats from the YoMaHa07
	product



	Dataframe columns:

	"Deep velocity estimates"

	lon_d : Deep vel. longitude
	lat_d : Deep vel. latitude
	p_d   : Parking pressure for this cycle
	t_d   : Julian time (relative to 2000-01-01 00:00 UTC)
	u_d   : Estimate of zonal velocity (cm s-1)
	v_d   : Estimate of meridional velocity (cm s-1) 
	eu_d  : Estimates of u errors
	ev_d  : Estimates of v errors


	"Surface velocity estimates"

	lon_s : Longitude 
	lat_s : Latitude
	t_s   : Julian time (relative to 2000-01-01 00:00 UTC)
	u_s   : Estimate of zonal velocity (cm s-1)
	v_s   : Estimate of meridional velocity (cm s-1)
	eu_s  : Estimates of u errors
	ev_s  : Estimates of v errors


	"Auxiliary float and cycle data"
	
	(Values for the last fix at the sea surface during the previous cycle)

	lon_lp : Longitude
	lat_lp : Latitude
	t_lp   : Julian time (relative to 2000-01-01 00:00 UTC)



	(Values for the first fix at the sea surface during the current cycle)

	lon_fc : Longitude
	lat_fc : Latitude
	t_fc   : Julian time (relative to 2000-01-01 00:00 UTC)
		


	(Values for the last fix at the sea surface during the current cycle)

	lon_lc : Longitude
	lat_lc : Latitude
	t_lc   : Julian time (relative to 2000-01-01 00:00 UTC)
	s_fix  : Number of surface fixes during the current cycle

	id     : Float Id
	cycle  : Cycle Number

	t_inv  : Time inversion / duplication: is equal to 1 if at least one duplicate 
	or inversion of time is found in the sequence containing last fix from the previous 
	cycle and all fixes from the current cycle. Otherwise the values is 0.




	Missing values: 
	
	Longitudes          : -999.9999
	Latitudes           : -99.9999
	Julian times        : -999.9999
	parking pressure    : -999.9
	velocity components : -999.99
	velocity errors     : -999.99
	"""


	## Dependencies
	import pandas
	import numpy as np

	## Parse data with Pandas
	col_names = ['lon_d', 'lat_d', 'p_d', 't_d',
		'u_d', 'v_d', 'eu_d', 'ev_d',
		'lon_s', 'lat_s', 't_s',
		'u_s', 'v_s', 'eu_s', 'ev_s',
		'lon_lp', 'lat_lp', 't_lp',
		'lon_fc', 'lat_fc', 't_fc', 
		'lon_lc', 'lat_lc', 't_lc',
		's_fix', 'id', 'cycle', 't_inv']

	na_col = [-999.9999, -99.9999, -999.9, -999.9999, 
		-999.99, -999.99, -999.99, -999.99,
		-999.99, -99.99, -999.99, 
		-999.99, -999.99, -999.99, -999.99,
		-999.99, -99.99, -999.99, 
		-999.99, -99.99, -999.99,
		-999.99, -99.99, -999.99,
		np.nan, np.nan, np.nan, np.nan]

	df = pandas.read_csv(filename, names=col_names, sep='\s+',
		header=None, na_values=na_col)


	return df

