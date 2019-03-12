#!/usr/bin/env python

import requests
import sys
import json
import os

from requests.packages.urllib3.exceptions import InsecureRequestWarning

vmanage_host = os.environ.get("vmanage_host")
vmanage_port = os.environ.get("vmanage_port")
username = os.environ.get("username")
password = os.environ.get("password")


if vmanage_host is None or vmanage_port is None or username is None or password is None:
    print("vManage details must be set via environment variables. For example: ")
    print("export vmanage_host=sdwandemo.cisco.com")
    print("export vmanage_port=8443")
    print("export username=demo")
    print("export password=demo")
    exit()

requests.packages.urllib3.disable_warnings()

class rest_api_lib:
    def __init__(self, vmanage_host,vmanage_port, username, password):
        self.vmanage_host = vmanage_host
        self.vmanage_port = vmanage_port
        self.session = {}
        self.login(self.vmanage_host, username, password)

    def login(self, vmanage_host, username, password):
        
        """Login to vmanage"""

        base_url = 'https://%s:%s/'%(self.vmanage_host, self.vmanage_port)

        login_action = '/j_security_check'

        #Format data for loginForm
        login_data = {'j_username' : username, 'j_password' : password}

        #Url for posting login data
        login_url = base_url + login_action
        url = base_url + login_url

        sess = requests.session()

        #If the vmanage has a certificate signed by a trusted authority change verify to True
        login_response = sess.post(url=login_url, data=login_data, verify=False)

        #print(sess.cookies)
    
        if b'<html>' in login_response.content:
            print ("Login Failed")
            sys.exit(0)

        self.session[vmanage_host] = sess


    def post_request(self, mount_point, payload, headers={'Content-type': 'application/json', 'Accept': 'application/json'}):
        """POST request"""
        url = "https://%s:%s/dataservice/%s"%(self.vmanage_host, self.vmanage_port, mount_point)
        #print(url)
        payload = json.dumps(payload)

        response = self.session[self.vmanage_host].post(url=url, data=payload, headers=headers, verify=False)

        return response


#Create session with vmanage 

vmanage_session = rest_api_lib(vmanage_host, vmanage_port, username, password)

#Fetch alarms for interval of 6 mins

query = {"query":{"condition":"AND","rules":[{"value":["2019-03-10T04:51:00 UTC","2019-03-10T04:57:00 UTC"],"field":"entry_time","type":"date","operator":"between"}]},"size":10000}

response = vmanage_session.post_request("alarms",query)

alarms = response.json()['data']

print("\n\nFetch alarms for interval of 6 mins\n\n" , alarms)


#Fetch alarms after it has been cleared

query = {"query":{"condition":"AND","rules":[{"value":["2019-03-10T04:57:00 UTC","2019-03-10T04:58:00 UTC"],"field":"entry_time","type":"date","operator":"between"},{"value":["Medium","Critical"],"field":"severity","type":"string","operator":"in"},{"value":["false"],"field":"active","type":"string","operator":"in"}]},"size":10000}

response = vmanage_session.post_request("alarms",query)

alarms = response.json()['data']

print("\n\nFetch alarms after it has been cleared\n\n",alarms)

#Fetch cleared alarms using filters

query = {"query":{"condition":"AND","rules":[{"value":["2019-03-10T04:57:00 UTC","2019-03-10T04:58:00 UTC"],"field":"entry_time","type":"date","operator":"between"},{"value":["Medium","Critical"],"field":"severity","type":"string","operator":"in"},{"value":["false"],"field":"active","type":"string","operator":"in"}]},"size":10000}

response = vmanage_session.post_request("alarms",query)

alarms = response.json()['data']

print("\n\nFetch cleared alarms using filters\n\n",alarms)

#Fetch cleared alarms using filters

query = {"query":{"condition":"AND","rules":[{"value":["2019-03-10T04:50:00 UTC","2019-03-10T04:57:00 UTC"],"field":"entry_time","type":"date","operator":"between"},{"value":["Medium","Critical"],"field":"severity","type":"string","operator":"in"},{"value":["false"],"field":"active","type":"string","operator":"in"}]},"size":10000}

response = vmanage_session.post_request("alarms",query)

alarms = response.json()['data']

print("\n\nFetch cleared alarms using filters\n\n",alarms)

#Fetch active alarms using filters

query = {"query":{"condition":"AND","rules":[{"value":["2019-03-10T04:50:00 UTC","2019-03-10T04:57:00 UTC"],"field":"entry_time","type":"date","operator":"between"},{"value":["Medium","Critical"],"field":"severity","type":"string","operator":"in"},{"value":["true"],"field":"active","type":"string","operator":"in"}]},"size":10000}

response = vmanage_session.post_request("alarms",query)

#No active alarms so no data returned from vManage

alarms = response.json()['data']

print("\n\nFetch active alarms using filters (No active alarms so no data returned from vManage)\n\n",alarms)

#Fetch Active Criticial, Major, Medium, Minor alarms between interval of 1 hour. 

query = {"query":{"condition":"AND","rules":[{"value":["2019-03-10T20:00:00 UTC","2019-03-10T21:00:00 UTC"],"field":"entry_time","type":"date","operator":"between"},{"value":["Critical","Major","Medium","Minor"],"field":"severity","type":"string","operator":"in"},{"value":["true"],"field":"active","type":"string","operator":"in"}]},"size":10000}

response = vmanage_session.post_request("alarms",query)

alarms = response.json()['data']

print("\n\nFetch Active Criticial, Major, Medium, Minor alarms between interval of 1 hour\n\n",alarms)

#Fetch based on name in alarm i.e. "Pseudo Commit Status"

query = {"query":{"condition":"AND","rules":[{"value":["2019-03-10T20:00:00 UTC","2019-03-10T21:00:00 UTC"],"field":"entry_time","type":"date","operator":"between"},{"value":["Critical","Major","Medium","Minor"],"field":"severity","type":"string","operator":"in"},{"value":["true"],"field":"active","type":"string","operator":"in"},{"value":["Pseudo_Commit_Status"],"field":"rule_name_display","type":"string","operator":"in"}]},"size":10000}

response = vmanage_session.post_request("alarms",query)

alarms = response.json()['data']

print("\n\nFetch based on name in alarm i.e. Pseudo Commit Status\n\n",alarms)


