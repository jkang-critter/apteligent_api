import json
import requests
import apteligent
import conf
import csv

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

instance = apteligent.restapi.Client(conf.credentials.hostname, conf.credentials.username, conf.credentials.password, conf.credentials.oauthToken)
apps = instance.get_apps()
appids = list(apps.keys())

#Takes in a list of app IDs and returns the data after the performanceManagementPie call is made. Remove any metrics that are not of relevance from metrics.
def run_performanceManagement(appids):
	metrics = ['dataIn', 'dataOut', 'latency', 'volume', 'errors']
	perf_data = []

	for appId in appids:
		for metric in metrics:
			appName = apps[appId]['appName']
			perf_data.append(instance.performanceManagementPie(
				appids=[appId],
				metric=metric,
				groupby='service'))

	return perf_data

with open('data_perf.csv', 'w+') as output_file_perf:
	output_writer_perf = csv.writer(output_file_perf, dialect='excel')
	data_perf = run_performanceManagement(appids)
	
	#Write header row to Excel file
	output_writer_perf.writerow(['appID', 'Graph', 'Duration (in min)', 'Group By', 'Service Name', 'Value', 'Label'])
	
	#Go through each line in Performance Management data and format 
	for row in data_perf:
		appID = row['params']['appIds']
		graph = row['params']['graph']
		duration = row['params']['duration']
		groupby = row['params']['groupby']

		for item in row['data']['slices']:
			row_format_perf = [appID, graph, duration, groupby, item['name'], item['value'], item['label']]
			output_writer_perf.writerow(row_format_perf)