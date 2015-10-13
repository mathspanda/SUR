'''
Created on Oct 13, 2015

'''

import requests


class CadvisorUtils(object):
    
    def __init__(self, host='localhost', port='8080'):
        self.url = 'http://%s:%s/api/v2.0' % (host, port)
        
    def __get_machine_info(self):
        machine_info_url = '%s/%s' % (self.url, 'machine')
        machine_info = requests.get(machine_info_url).json()
        return machine_info
    
    def get_machine_memory(self):
        return self.__get_machine_info()['topology'][0]['memory']
    
    def __get_containers_stats(self, count=1):
        stats_url = '%s/%s?count=%s' % (self.url, 'stats', count)
        stats_info = requests.get(stats_url).json()
        return stats_info
    
    def get_containers_memory_usage(self):
        return self.__get_containers_stats()['/'][0]['memory']['usage']

    