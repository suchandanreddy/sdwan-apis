# vManage REST API’s

  - REpresentational State Transfer (REST) is an architecture style for designing web-services applications
  - REST architecture uses a stateless, client–server, cacheable communications protocol.
  - The vManage web server uses HTTP and its secure counterpart, HTTPS, as the communications protocol
  - vManage API Documentation is built-in at https://<vmanage-ip:port>/apidocs
  - Test API calls can be tried out from swagger UI at /apidocs
  
# URL Structure Components

  - URL to fetch alarms is https://<vmanage-ip:port>/dataservice/alarms 

|  |  |
| ------ | ------ |
| http:// or https://  | Protocol over which data is sent  between client and server |
| Server or Host  | Resolves to the IP and port to which to connect, example : "<vmanage-ip:port>" |
| Resource | The location of the data or object of  interest, example : "dataservice/alarms" |
| Parameters  | Details to scope, filter, or clarify a request. Often optional|

Example for Parameters
  -   URL : https://<vmanage-ip:port>/dataservice/device/bfd/state/device?deviceId=1.1.1.7 
  -   "?deviceId=1.1.1.7" is used to filter out bfd state for device with system-ip/deviceId = 1.1.1.7

Now let’s start using the python script to fetch the alarms by using below steps:

  - login and authenticate to a vManage instance
  - Build Query to specify the rules and how to collect alarms
  - Perform the POST operation by sending query in payload

# Authentication

Input parameters for login function are

-  endpoint vManage i.e. https://{{vmanage}}:{{port}} 
-  login resource URL i.e. /j_security_check. 

The vManage username and password are specified using dictionary variable.

On successful POST operation we get JSESSIONID or cookie which is used in future API calls by client. By nature REST API is stateless so we use JSESSIONID for doing session tracking.

To get cookie check out "sess.cookies" which would contain JSESSIONID 

```
import requests
sess = requests.session()
Now after login check sess.cookies for JESSIONID value
```

# Login Function

```
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
```

Now let’s define the Query which can be used to collect alarms using POST operation on "dataservice/alarms"

#   Query Payload

Samples on how to build Query payload to retrieve alarms

#   Example-1

Between operator can be used to fetch the alarms for a custom interval for example i.e. 4:51:00 UTC to 4:57:00 UTC ( 6 mins interval )

```
{
  "query": {
    "condition": "AND",         # Logical AND Operation among rules defined below
    "rules": [
      {
        "value": [              # Alarms between 04:51:00 and 04:57:00 on 10/03/2019
          "2019-03-10T04:51:00 UTC",
          "2019-03-10T04:57:00 UTC"
        ],
        "field": "entry_time",
        "type": "date",
        "operator": "between"
      }
    ]
  },
  "size": 10000
}
```

#   Example-2  

Collect only cleared Medium, Critical alarms between 4:57 and 4:58

```
{
  "query": {
    "condition": "AND",      # Logical AND Operation among rules defined below
    "rules": [
      {
        "value": [           # Alarms between 04:51:00 and 04:57:00 on 10/03/2019
          "2019-03-10T04:57:00 UTC",
          "2019-03-10T04:58:00 UTC"
        ],
        "field": "entry_time",
        "type": "date",
        "operator": "between"
      },
      {
        "value": [           # Only alarms with severity level Critical and Medium 
          "Medium",
          "Critical"
        ],
        "field": "severity",
        "type": "string",
        "operator": "in"
      },
      {
        "value": [   
          "false"       # Value is set to false for Cleared alarms and True for active alarms
        ],
        "field": "active",
        "type": "string",
        "operator": "in"
      }
    ]
  },
  "size": 10000
}

```

# Example-3

Collect *Active* Critical, Major, Medium, Minor alarms related to "Pseudo Commit Status" between 20:00 and 21:00

```

{
  "query": {
    "condition": "AND",         # Logical AND Operation among rules defined below
    "rules": [
      {
        "value": [              # Alarms between 20:00:00 and 21:00:00 on 10/03/2019
          "2019-03-10T20:00:00 UTC",
          "2019-03-10T21:00:00 UTC"
        ],
        "field": "entry_time",
        "type": "date",
        "operator": "between"
      },
      {
        "value": [              # Alarms with severity level Critical, Major, Medium, Minor
          "Critical",
          "Major",
          "Medium",
          "Minor"
        ],
        "field": "severity",
        "type": "string",
        "operator": "in"
      },
      {
        "value": [              # Value is set to true for Active alarms
          "true"
        ],
        "field": "active",
        "type": "string",
        "operator": "in"
      },
      {
        "value": [              # Pseudo Commit Status alarms are retrieved
          "Pseudo_Commit_Status"
        ],
        "field": "rule_name_display",
        "type": "string",
        "operator": "in"
      }
    ]
  },
  "size": 10000
}

```

Using this Query lets perform POST operation on URI to retrieve the alarms.

#   POST Operation

To fetch the alarms we need to perform POST operation using request method from the python requests library.
Input parameters for POST operation
-   endpoint (vmanage server ip address)
-   resource or mountpoint represented by the URL
-   headers (Content-type and Accept are set to application/json)
-   The query which defines how alarms are collected is sent using the payload. 

"verify=False" parameter is passed in POST operation because the SSL verification is disabled.

The result of the POST operation is stored in the response variable. The json() method is called on the response object and the JSON format of the response is returned. "data" key in the JSON output contains the alarm details retrieved.

```
def post_request(self, mount_point, payload, headers={'Content-type': 'application/json', 'Accept': 'application/json'}):

        """POST request"""
        url = "https://%s:%s/dataservice/%s"%(self.vmanage_host, self.vmanage_port, mount_point)
        payload = json.dumps(payload)
        response = self.session[self.vmanage_host].post(url=url, data=payload, headers=headers, a)
        return response
```

Now let's have a look at the responses to POST operation

### Sample Responses

-   Every alarm can be uniquely identified based on the uuid value which is associated with it. 
-   In case alarm is cleared in another interval then uuid of alarm which has cleared it is associated with key  “cleared_by” and cleared time is associated with key “cleared_time”

#   Example-1

```
"data": [
    {
      "devices": [
        {
          "system-ip": "1.1.1.15"
        }
      ],
      "eventname": "interface-state-change",
      "type": "interface-state-change",
      "rulename": "interface-state-change",
      "component": "VPN",
      "entry_time": 1552193785000,
      "statcycletime": 1552193785000,
      "message": "The interface oper-state changed to down",
      "severity": "Critical",
      "severity_number": 1,
      "uuid": "9f75552d-4a2b-4085-9dcc-fd15148cf078",  
      "values": [
        {
          "host-name": "Azure-Gateway-West",
          "system-ip": "1.1.1.15",
          "if-name": "ipsec4",
          "new-state": "down",
          "vpn-id": "1"
        }
      ],
      "rule_name_display": "Interface_State_Change",
      "receive_time": 1552194337469,
      "values_short_display": [
        {
          "host-name": "Azure-Gateway-West",
          "system-ip": "1.1.1.15",
          "if-name": "ipsec4",
          "new-state": "down"
        }
      ],
      "acknowledged": false,
      "active": false,
      "tenant": "default",
      "cleared_by": "36af5221-d248-4aef-bed6-0f9a59b30f98", 
      "cleared_time": 1552193878000,
      "id": "AWll_frUhE4U7yO21aG1"
    },
    {
      "devices": [
        {
          "system-ip": "1.1.1.14"
        }
      ],
      "eventname": "interface-state-change",
      "type": "interface-state-change",
      "rulename": "interface-state-change",
      "component": "VPN",
      "entry_time": 1552193772000,
      "statcycletime": 1552193772000,
      "message": "The interface oper-state changed to down",
      "severity": "Critical",
      "severity_number": 1,
      "uuid": "08dd7b00-3893-4809-9e22-1351a9f81776",
      "values": [
        {
          "host-name": "Azure-Gateway-West",
          "system-ip": "1.1.1.14",
          "if-name": "ipsec4",
          "new-state": "down",
          "vpn-id": "1"
        }
      ],
      "rule_name_display": "Interface_State_Change",
      "receive_time": 1552194337697,
      "values_short_display": [
        {
          "host-name": "Azure-Gateway-West",
          "system-ip": "1.1.1.14",
          "if-name": "ipsec4",
          "new-state": "down"
        }
      ],
      "acknowledged": false,
      "active": false,
      "tenant": "default",
      "cleared_by": "dec318ae-9b3e-4913-a083-6e4549ca710e",   ## Cleared Alarm uuid
      "cleared_time": 1552193864000,                          ## Cleared time
      "id": "AWll_fu3hE4U7yO21aG3"
    }
  ]
  
```

# Example-2

Response which has both Active and Cleared alarms. Alarms can be correlated further based on uuid value. For example we can see alarm with uuid "36af5221-d248-4aef-bed6-0f9a59b30f98" is a cleared event which indicates *"The interface oper-state changed to up"* , The alarm that got cleared is provided by list of uuids in *cleared_events* : 9f75552d-4a2b-4085-9dcc-fd15148cf078

```
  {
    "devices": [
      {
        "system-ip": "1.1.1.15"
      }
    ],
    "eventname": "interface-state-change",
    "type": "interface-state-change",
    "rulename": "interface-state-change",
    "component": "VPN",
    "entry_time": 1552193878000,
    "statcycletime": 1552193878000,
    "message": "The interface oper-state changed to up",
    "severity": "Medium",
    "severity_number": 3,
    "uuid": "36af5221-d248-4aef-bed6-0f9a59b30f98",
    "values": [
      {
        "host-name": "Azure-Gateway-West",
        "system-ip": "1.1.1.15",
        "if-name": "ipsec4",
        "new-state": "up",
        "vpn-id": "1"
      }
    ],
    "rule_name_display": "Interface_State_Change",
    "receive_time": 1552194429966,
    "values_short_display": [
      {
        "host-name": "Azure-Gateway-West",
        "system-ip": "1.1.1.15",
        "if-name": "ipsec4",
        "new-state": "up"
      }
    ],
    "acknowledged": false,
    "cleared_events": [                     # list of uuid's which got cleared by this alarm
      "9f75552d-4a2b-4085-9dcc-fd15148cf078"
    ],
    "active": false,
    "tenant": "default",
    "id": "AWll_2RIhE4U7yO21aHG"
  },
  {
    "devices": [
      {
        "system-ip": "1.1.1.14"
      }
    ],
    "eventname": "interface-state-change",
    "type": "interface-state-change",
    "rulename": "interface-state-change",
    "component": "VPN",
    "entry_time": 1552193864000,
    "statcycletime": 1552193864000,
    "message": "The interface oper-state changed to up",
    "severity": "Medium",
    "severity_number": 3,
    "uuid": "dec318ae-9b3e-4913-a083-6e4549ca710e",
    "values": [
      {
        "host-name": "Azure-Gateway-West",
        "system-ip": "1.1.1.14",
        "if-name": "ipsec4",
        "new-state": "up",
        "vpn-id": "1"
      }
    ],
    "rule_name_display": "Interface_State_Change",
    "receive_time": 1552194429392,
    "values_short_display": [
      {
        "host-name": "Azure-Gateway-West",
        "system-ip": "1.1.1.14",
        "if-name": "ipsec4",
        "new-state": "up"
      }
    ],
    "acknowledged": false,
    "cleared_events": [
      "08dd7b00-3893-4809-9e22-1351a9f81776"
    ],
    "active": false,
    "tenant": "default",
    "id": "AWll_2H6hE4U7yO21aHE"
  },
  {
    "devices": [
      {
        "system-ip": "1.1.1.15"
      }
    ],
    "eventname": "interface-state-change",
    "type": "interface-state-change",
    "rulename": "interface-state-change",
    "component": "VPN",
    "entry_time": 1552193785000,
    "statcycletime": 1552193785000,
    "message": "The interface oper-state changed to down",
    "severity": "Critical",
    "severity_number": 1,
    "uuid": "9f75552d-4a2b-4085-9dcc-fd15148cf078",
    "values": [
      {
        "host-name": "Azure-Gateway-West",
        "system-ip": "1.1.1.15",
        "if-name": "ipsec4",
        "new-state": "down",
        "vpn-id": "1"
      }
    ],
    "rule_name_display": "Interface_State_Change",
    "receive_time": 1552194337469,
    "values_short_display": [
      {
        "host-name": "Azure-Gateway-West",
        "system-ip": "1.1.1.15",
        "if-name": "ipsec4",
        "new-state": "down"
      }
    ],
    "acknowledged": false,
    "active": false,
    "tenant": "default",
    "cleared_by": "36af5221-d248-4aef-bed6-0f9a59b30f98",
    "cleared_time": 1552193878000,
    "id": "AWll_frUhE4U7yO21aG1"
  },
  {
    "devices": [
      {
        "system-ip": "1.1.1.14"
      }
    ],
    "eventname": "interface-state-change",
    "type": "interface-state-change",
    "rulename": "interface-state-change",
    "component": "VPN",
    "entry_time": 1552193772000,
    "statcycletime": 1552193772000,
    "message": "The interface oper-state changed to down",
    "severity": "Critical",
    "severity_number": 1,
    "uuid": "08dd7b00-3893-4809-9e22-1351a9f81776",
    "values": [
      {
        "host-name": "Azure-Gateway-West",
        "system-ip": "1.1.1.14",
        "if-name": "ipsec4",
        "new-state": "down",
        "vpn-id": "1"
      }
    ],
    "rule_name_display": "Interface_State_Change",
    "receive_time": 1552194337697,
    "values_short_display": [
      {
        "host-name": "Azure-Gateway-West",
        "system-ip": "1.1.1.14",
        "if-name": "ipsec4",
        "new-state": "down"
      }
    ],
    "acknowledged": false,
    "active": false,
    "tenant": "default",
    "cleared_by": "dec318ae-9b3e-4913-a083-6e4549ca710e",
    "cleared_time": 1552193864000,
    "id": "AWll_fu3hE4U7yO21aG3"
  }
]
```

entry_time, cleared_time values are in epoch format.

Use time function to convert epoch values to format MM-DD-YYYY HH-MM-SS format

```
>>> entry_time = 1552309200000
>>> time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(entry_time/1000.))
'03/11/2019 13:00:00'
>>>
```

Complete script can be accessed [here](https://github.com/suchandanreddy/sdwan-apis/blob/master/alarms_api.py)

                                                                            [Next: Webhook](webhooks/webhook.md)
