#!/usr/bin/env python

import requests
from thehive4py.api import TheHiveApi
from thehive4py.query import Id

### variables ###
api_key = "xxx"
url = "http://123.123.123.132:9000"

caseId = 'AXHqneDzwVzwaw7unmbD'
#################

def main():
    api = TheHiveApi(url, api_key)

    session = requests.Session()
    session.headers.update({"Authorization": "Bearer {}".format(api_key)})

    obs = api.get_case_observables(
        caseId, query={}, sort=["-startDate", "+ioc"], range="all"
    )
    obs = obs.json()
    for ob in obs:
        r = session.get('{}/api/case/artifact/{}/similar?range=all&sort=-startDate'.format(url, ob['id']))
        data = r.json()
        if len(data) > 0:
            print(ob['data'], len(r.json()), 'results')
            titles = []
            for case in data:
                #print(case)
                cases = api.find_cases(query=Id(case['_parent']), range="all")
                print("\t - {} [{}]".format(cases.json()[0]['title'], case['_parent']))
            print()
            


if __name__ == "__main__":
    print("[INFO] Starting the script...")
    main()
    print("[INFO] Program terminated. Exiting...")
