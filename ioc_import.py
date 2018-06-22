#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Script that parses text file for import IOC in a new case directly in The Hive 
#Requires ioc_parser (https://github.com/armbues/ioc_parser) and thehive4py (sudo pip install thehive4py)
#version 1.0
#license AGPL-V3
#authors: garanews, dadokkio


from __future__ import print_function
from __future__ import unicode_literals

import requests
import os
import sys
import json
import time
import argparse
import subprocess

from thehive4py.api import TheHiveApi
from thehive4py.models import Case, CaseTask, CaseObservable

exchange = {
    'Host': 'domain',
    'Filename': 'filename',
    'SHA256': 'hash',
    'SHA1': 'hash',
    'MD5': 'hash',
    'Email': 'mail',
    'URL': 'url',
    'IP': 'ip'
}

class THApi:

    def __init__(self, filepath):
        self.api = TheHiveApi('http://THE_HIVE_IP:PORT', 'API_KEY')
        self.case_id = None
        self.osservable_data = []
        self.filepath = filepath
        self.filetype = filepath.split(".")[-1]
        self.filename = os.path.basename(filepath)

    def run_iocp(self):
        data = []
        proc = subprocess.Popen(['iocp', '-i', self.filetype, self.filepath], stdout=subprocess.PIPE)
        for line in proc.stdout.readlines():
            self.osservable_data.append([x for x in line.strip().split(',') if line.strip() != ''])

    def create_osservables(self):
        for oss in self.osservable_data:
            domain = CaseObservable(dataType=exchange[oss[2]], tlp=1, ioc=True, tags=['thehive4py'], data=oss[3] )
            response = self.api.create_case_observable(self.case_id, domain)
            if response.status_code == 201:
                print(json.dumps(response.json(), indent=4, sort_keys=True))
                print('')
            else:
                print('ko: {}/{}'.format(response.status_code, response.text))

            print ("adding OSSERVABLE", oss[2], "-", oss[3] , "to", self.case_id)

    def create_case(self):
        case = Case(title='From TheHive4Py', tlp=3, flag=True, tags=['TheHive4Py', 'sample'], description=self.filename)
        response = self.api.create_case(case)
        if response.status_code == 201:
            self.case_id =  response.json()['id']
        else:
            self.case_id = None

    def plot_case(self):
        response = self.api.get_case(self.case_id)
        print(json.dumps(response.json(), indent=4, sort_keys=True))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Welcome')
    parser.add_argument('filepath', help='an integer for the accumulator')
    args = parser.parse_args()
    th = THApi(args.filepath)
    th.run_iocp()
    if len(th.osservable_data) > 0:
        th.create_case()
        th.create_osservables()
        th.plot_case()

