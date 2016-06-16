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

#Takes in a list of app IDs and returns the data after the errorMonitoringGraph call is made. Remove any metrics that are not of relevance from metrics.
#If a longer duration is desired, change duration parameter in the errorMonitoringGraph method call.
def run_errorMonitoringGraph(appids):
	metrics = ['crashPercent', 'mau', 'dau', 'rating', 'appLoads', 'crashes', 'affectedUsers', 'affectedUserPercent']
	errorMon_data = []

	for appId in appids:	
		for metric in metrics:
			appName = apps[appId]['appName']
			path = [conf.credentials.metric_root, appName, 'daily', metric]
			errorMon_data.append(instance.errorMonitoringGraph(appid=appId, metric=metric, duration=1440))

	return errorMon_data

with open('data_error.csv', 'w+') as output_file_error:
	output_writer_error = csv.writer(output_file_error, dialect='excel')
	data_error = run_errorMonitoringGraph(appids)
	output_writer_error.writerow(['appID', 'Graph', 'Duration (in min)', 'Value'])
	for row in data_error:
		appID = row['params']['appId']
		graph = row['params']['graph']
		duration = row['params']['duration']
		points = row['data']['series'][0]['points']
		row_format_error = [appID, graph, duration, points[0]]
		output_writer_error.writerow(row_format_error)
