from influxdb import InfluxDBClient
import requests
import sys
import json
import os
import pprint
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning

vmanage_host = os.environ.get("vmanage_host")
vmanage_port = os.environ.get("vmanage_port")
username = os.environ.get("username")
password = os.environ.get("password")


if vmanage_host is None or vmanage_port is None or username is None or password is None:
    print("For Windows Workstation, vManage details must be set via environment variables using below commands")
    print("set vmanage_host=198.18.1.10")
    print("set vmanage_port=443")
    print("set username=admin")
    print("set password=admin")
    print("For MAC OSX Workstation, vManage details must be set via environment variables using below commands")
    print("export vmanage_host=198.18.1.10")
    print("export vmanage_port=443")
    print("export username=admin")
    print("export password=admin")
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

    
        if b'<html>' in login_response.content:
            print ("Login Failed")
            sys.exit(0)

        self.session[vmanage_host] = sess

    def get_request(self, mount_point):
        """GET request"""
        url = "https://%s:%s/dataservice/%s"%(self.vmanage_host, self.vmanage_port, mount_point)
        print(url)
      
        response = self.session[self.vmanage_host].get(url, verify=False)
        
        return response

    def post_request(self, mount_point, payload, headers={'Content-type': 'application/json', 'Accept': 'application/json'}):
        """POST request"""
        url = "https://%s:%s/dataservice/%s"%(self.vmanage_host, self.vmanage_port, mount_point)
        #print(url)
        payload = json.dumps(payload)
        #print (payload)

        response = self.session[self.vmanage_host].post(url=url, data=payload, headers=headers, verify=False)
        #print(response.text)
        #exit()
        #data = response
        return response




vmanage_session = rest_api_lib(vmanage_host, vmanage_port, username, password)

payload = {"aggregation":{"metrics":[{"property":"fw_total_insp_count","type":"sum","order":"desc"}],"histogram":{"property":"entry_time","type":"minute","interval":30,"order":"asc"}},"query":{"condition":"AND","rules":[{"value":["24"],"field":"entry_time","type":"date","operator":"last_n_hours"},{"value":["total"],"field":"type","type":"string","operator":"in"}]}}

response = vmanage_session.post_request("statistics/fwall/aggregation",payload)

items = response.json()['data']



#login credentials for InfluxDB

USER = 'root'
PASSWORD = 'root'
DBNAME = 'firewall_inspect'


host='localhost'
port=8086

series = []
total_records = 0

json_body = {}

#loop over the API response variable items and create records to be stored in InfluxDB

for i in items:
    json_body = { "measurement": "firewall_inspect_count",
                  "tags": {
                            "host": "wan_edge",
                          },
                 "time": time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(i['entry_time']/1000.)),
                 "fields": {
                            "value": float(i['fw_total_insp_count'])
                }
                }
    series.append(json_body)
    total_records = total_records+1

client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)

print("Create a retention policy")
retention_policy = 'retention_policy_1'
client.create_retention_policy(retention_policy, '10d', 3, default=True)

print("Write points #: {0}".format(total_records))
client.write_points(series, retention_policy=retention_policy)

time.sleep(2)