import requests
import json
import os
import tabulate
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import urlencode


from requests.packages.urllib3.exceptions import InsecureRequestWarning

vmanage_host = os.environ.get("vmanage_host")
vmanage_port = os.environ.get("vmanage_port")
username = os.environ.get("username")
password = os.environ.get("password")
gmail_username = os.environ.get("gmail_username")
gmail_password = os.environ.get("gmail_password")
sender_address = os.environ.get("sender_address")
to_address = os.environ.get("to_address")

if vmanage_host is None or vmanage_port is None or username is None or password is None or gmail_username is None or gmail_password is None or sender_address is None or to_address is None :
    print("For Windows Workstation, vManage details must be set via environment variables using below commands")
    print("set vmanage_host=198.18.1.10")
    print("set vmanage_port=443")
    print("set username=admin")
    print("set password=admin")
    print("set gmail_username=<gmail username>")
    print("set gmail_password=<gmail password>")
    print("set sender_address=<email sender address>")
    print("set to_address=<email receiver address>")
    print("For MAC OSX Workstation, vManage details must be set via environment variables using below commands")
    print("export vmanage_host=198.18.1.10")
    print("export vmanage_port=443")
    print("export username=admin")
    print("export password=admin")
    print("export gmail_username=<gmail username>")
    print("export gmail_password=<gmail password>")
    print("export sender_address=<email sender address>")
    print("export to_address=<email receiver address>")
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

        login_action = 'j_security_check'

        #Format data for loginForm
        login_data = {'j_username' : username, 'j_password' : password}

        #Url for posting login data
        login_url = base_url + login_action
        #url = base_url + login_url

        #URL for retrieving client token
        token_url = base_url + 'dataservice/client/token'

        sess = requests.session()

        #If the vmanage has a certificate signed by a trusted authority change verify to True

        login_response = sess.post(url=login_url, data=login_data, verify=False)
        
        if b'<html>' in login_response.content:
            print ("Login Failed")
            exit(0)

        login_token  = sess.get(url=token_url, verify=False)

        if login_token.status_code == 200:
            if b'<html>' in login_token.content:
                print ("Login Token Failed")
                exit(0)

        #update token to session headers
        sess.headers['X-XSRF-TOKEN'] = login_token.content

        self.session[vmanage_host] = sess

    def get_request(self, mount_point):
        """GET request"""
        url = "https://%s:%s/dataservice/%s"%(self.vmanage_host, self.vmanage_port, mount_point)
        #print(url)
      
        response = self.session[self.vmanage_host].get(url,verify=False)
        
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

#Fetching list of device templates

'''query = {"query":{"condition":"AND",
                  "rules":[
                      { "value":["24"],
                        "field":"entry_time",
                        "type":"date",
                        "operator":"last_n_hours"},
                      {"value":["1.1.1.6"],
                       "field":"vdevice_name",
                       "type":"string",
                       "operator":"in"},
                      {"value":["web"],
                       "field":"family",
                       "type":"string",
                       "operator":"in"},
                      {"value":["web"],
                       "field":"family",
                       "type":"string",
                       "operator":"in"}]},
                  "aggregation":{"field":[{"property":"application","size":200,"sequence":1}],
                                 
                                 "metrics":[{"property":"octets","type":"sum","order":"desc"}]}}'''

'''query = {
  "query": {
    "condition": "AND",
    "rules": [
      {
        "value": [
          "24"
        ],
        "field": "entry_time",
        "type": "date",
        "operator": "last_n_hours"
      },
      {
        "value": [
          "1.1.2.201"
        ],
        "field": "vdevice_name",
        "type": "string",
        "operator": "in"
      },
      {
        "value": [
          "dia"
        ],
        "field": "local_color",
        "type": "string",
        "operator": "in"
      }
    ]
  },
  "aggregation": {
    "field": [
                  {"property":"application",
                  "size":200,
                  "sequence":1},
                  {"property":"family",
                  "size":200,
                  "sequence":1},
                  {"property":"local_color",
                  "size":25,
                 "sequence":1
                 }
    ],
    "metrics": [
      {
        "property": "octets",
        "type": "sum",
        "order": "desc"
      }
    ]
  }
}'''

query = {
  "query": {
    "condition": "AND",
    "rules": [
      {
        "value": [
          "24"
        ],
        "field": "entry_time",
        "type": "date",
        "operator": "last_n_hours"
      },
      {
        "value": [
          "dia"
        ],
        "field": "local_color",
        "type": "string",
        "operator": "in"
      }
    ]
  },
  "aggregation": {
    "field": [
                  {"property":"application",
                  "size":200,
                  "sequence":1},
                  {"property":"family",
                  "size":200,
                  "sequence":1},
                  {"property":"local_color",
                  "size":25,
                 "sequence":1
                 },
                 {
                 "property": "vdevice_name",
        		 "type": "string"
    			 }
    ],
    "metrics": [
      {
        "property": "packets",
        "type": "sum",
        "order": "desc"
      }
    ]
  }
}
 


dpi_summary = vmanage_session.post_request("statistics/dpi/aggregation",query)

if dpi_summary.status_code == 200:
    print("\nDIA path application statistics\n")
    #print(dpi_summary.json()['data'])
    items = dpi_summary.json()['data']
else:
    print("\nError fetching DIA path application statistics\n")
    print(dpi_summary.status_code,dpi_summary.text)
    exit()

headers = ["System IP", "Application", "Application Family", "Packets"]

table = list()

for item in items:
    tr = [item['vdevice_name'], item['application'], item['family'], item['packets']]
    table.append(tr)
try:
    print(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
except UnicodeEncodeError:
    print(tabulate.tabulate(table, headers, tablefmt="grid"))


server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()

server.login(gmail_username,gmail_password)

mail_body = tabulate.tabulate(table, headers, tablefmt="html")

msg = MIMEMultipart('alternative')

msg['Subject'] = 'DIA path application statistics'
msg['From'] = sender_address
msg['To'] = to_address
Message=str(mail_body)
part2 = MIMEText(mail_body,'html')
msg.attach(part2)
server.sendmail(sender_address,to_address,msg.as_string())
server.quit()

print("\nSent email to ",to_address)