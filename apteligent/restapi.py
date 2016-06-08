import json
import requests

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

class Client(object):
    def __init__(self, hostname, username, password, oauthToken):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.oauthToken = oauthToken

        #self.token = cache('token')
        self.apps = None

    def all_bases(self):
        url = 'https://' + self.hostname + '/allyourbase'
        r = requests.get(url)
        r.raise_for_status()
        version = r.json()['versions']['v1']['latest']
        href = r.json()['links'][version]['href']
        return version, href

    def get_base(self, basepath):
        log.info('Retrieving list of API endpoints')
        url = 'https://' + self.hostname + basepath
        r = requests.get(url)
        log.debug(r.text)
        r.raise_for_status()
        return r.json()['links']

    def get_token(self):
        return 'Bearer ' + self.oauthToken

    '''
    def new_token(self):
        log.info('Getting a new authorization token from Apteligent')

        payload = {'grant_type': 'password', 'username': self.username, 'password': self.password}

        path = '/v1.0/token'
        url = "https://" + self.hostname + path
        r = requests.post(url, payload, auth=(self.clientID, ''))

        self.token.update(r.json())
        self.token.store()
    '''

    def appname(self, appID):
        return self.get_apps()[appID]['appName']

    def get_apps(self):
        apps = self.__get_apps([
            'appName'])
            #'linkToAppStore',
            #'appVersions',
            #'latestVersionString',
            #'iconURL'])

        self.apps = apps

        return self.apps

    def __get_apps(self, tracked_attributes):
        tokenstr = self.get_token()
        path = '/v1.0/apps'
        url = 'https://' + self.hostname + path
        attr = ','.join(tracked_attributes)

        r = requests.get(
            url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': tokenstr
            },
            params={'attributes': attr})

        apps = r.json()
        return apps

    def get_dailystats(self):
        tracked_attributes = ['appName',
                              'crashPercent',
                              'latency',
                              'mau',
                              'dau',
                              'rating']

        apps = self.__get_apps(tracked_attributes)
        return apps

    def performanceManagementPie(self, appids=None, duration=15, metric='volume', filterkey=None, filtervalue=None, groupby=None):
        if appids is None:
            appids = list(self.get_apps().keys())
        href = '/v1.0/performanceManagement/pie'
        url = 'https://' + self.hostname + href
        tokenstr = self.get_token()

        parameters = dict()
        parameters['params'] = {'appIds': appids, 'graph': metric, 'duration': duration}

        if groupby:
            parameters['params']['groupby'] = groupby
        if filterkey:
            parameters['params']['filters'] = {filterkey: filtervalue}

        payload = json.dumps(parameters)

        r = requests.post(url, data=payload, headers={'Content-Type': 'application/json', 'Authorization': tokenstr})

        return r.json()

    def errorMonitoringGraph(self, **kwargs):
        if 'metric' not in kwargs:
            kwargs['metric'] = 'crashes'
        return self.errorMonitoring('/v1.0/errorMonitoring/graph', **kwargs)

    def errorMonitoringPie(self, **kwargs):
        if 'metric' not in kwargs:
            kwargs['metric'] = 'appLoads'
        if 'grouby' not in kwargs:
            kwargs['groupby'] = 'appId'
        return self.errorMonitoring('/v1.0/errorMonitoring/pie', **kwargs)

    def errorMonitoringSparklines(self, **kwargs):
        if 'metric' not in kwargs:
            kwargs['metric'] = 'appLoads'
        if 'groupby' not in kwargs:
            kwargs['groupby'] = 'appId'
        return self.errorMonitoring('/v1.0/errorMonitoring/sparklines', **kwargs)

    def errorMonitoring(self, path, appid=None, appids=None, metric='appLoads',
                        duration=1440, filterkey=None, filtervalue=None,
                        groupby=None):

        url = 'https://' + self.hostname + path

        parameters = dict()
        parameters['params'] = {'graph': metric, 'duration': duration}
        if appid is None and appids is None:
            apps = self.get_apps()
            appids = list(apps.keys())
            parameters['params']['appIds'] = appids
        elif appids is None:
            parameters['params']['appId'] = appid

        tokenstr = self.get_token()

        if groupby:
            parameters['params']['groupBy'] = groupby
        if filterkey:
            parameters['params']['filters'] = {filterkey: filtervalue}

        payload = json.dumps(parameters)

        r = requests.post(url,
                          data=payload,
                          headers={'Content-Type': 'application/json',
                                   'Authorization': tokenstr})

        return r.json()

    def livestats_totals(self, app_id, app_version='total'):
        tokenstr = self.get_token()

        url = "https://{}/v1.0/liveStats/totals/{}".format(self.hostname,
                                                           app_id)
        r = requests.post(url,
                          headers={'Authorization': tokenstr},
                          params={'app_version': app_version})


        return r.json()