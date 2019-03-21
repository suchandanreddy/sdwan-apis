   * [vManage REST API's](#vmanage-rest-api's)
   * [Available API Calls](#available-api-calls)
   * [Authentication](#authentication)
   * [Login Function](#login-function)
   * [Device Inventory and Monitoring API's](#device-inventory-and-monitoring-apis)
   * [URL Structure Components](#url-structure-components)
   * [List Devices](#list-devices)
   * [Control Status](#control-status)
   * [Interface Status](#interface-status)
   * [Device Counters](#device-counters)
   * [System Status](#system-status)
   * [Configuration API's](#configuration-apis)
   * [Templates list](#templates-list)
   * [Create Templates](#create-templates)
   * [URL Structure Components](#url-structure-components-1)
   * [DPI statistics](#dpi-statistics)
   * [Example-2](#example-2)
   * [Example-3](#example-3)
   * [POST Operation](#post-operation)
   * [Sample Response](#sample-response)
   * [Influx DB:](#influx-db)
   * [Prerequisites](#prerequisites)
   * [Install InfluxDB](#install-influxdb)
   * [Installation Logs](#installation-logs)
   * [Connect to InfluxDB](#connect-to-influxdb)
   * [Install Grafana](#install-grafana)
   * [Installation Logs](#installation-logs-1)
   * [Configure Grafana](#configure-grafana)
   * [Create a Dashboard](#create-a-dashboard)
      * [Notes for mac](#notes-for-mac)
   * [Webhook](#webhook)
   * [Prerequisites](#prerequisites-1)
   * [Configure](#configure)
   * [Notifications Dashboard](#notifications-dashboard)
   * [Test Webhook](#test-webhook)
   * [Set up Webhook server on ubuntu](#set-up-webhook-server-on-ubuntu)
   * [Logs from Webhook Server:](#logs-from-webhook-server)
   * [Alarms on vManage](#alarms-on-vmanage)
   * [References](#references)
   * [Alarms API’s](#alarms-apis)
   * [URL Structure Components](#url-structure-components-2)
   * [Query Payload](#query-payload)
   * [Example-1](#example-1)
   * [Example-2](#example-2-1)
   * [Example-3](#example-3-1)
   * [POST Operation](#post-operation-1)
         * [Sample Responses](#sample-responses)
   * [Example-1](#example-1-1)
   * [Example-2](#example-2-2)


# vManage REST API's

  - REpresentational State Transfer (REST) is an architecture style for designing web-services applications
  - REST architecture uses a stateless, client–server, cacheable communications protocol.
  - The vManage web server uses HTTP and its secure counterpart, HTTPS, as the communications protocol
  - vManage API Documentation is built-in at https://<vmanage-ip:port>/apidocs
  - Test API calls can be tried out from swagger UI at /apidocs

# Available API Calls

- 	In REST API terminology, each of these features or operations is called a resource. 
-	A resource is an object with a type, associated data, relationships to other resources, and a set of methods that operate on it.
- Resources are grouped into collections. Each collection contains a single type of resource, and so is homogeneous

| Resource Collection | Resources for |
| ------ | ------ |		
| Device Action | Manage device actions viz. reboot, upgrade, lxcinstall etc. Resource URL: /device/action/|	
|Device Inventory | Retrieving device inventory information, including serial numbers and system status. Resource URL: /system/device |
| Administration | 	Managing users and user groups, viewing audit logs, and managing the local vManage server.
| Certificate Management | Managing certificates and security keys. Resource URL: /certificate|
| Configuration	| Creating feature and device configuration templates, retrieving the configurations in existing templates, and creating and configuring vManage clusters. Resource URL: /template/ , /template/policy/ |
| Monitoring	| Viewing status, statistics, and other information about operational devices in the overlay network. Monitoring information is what Viptela devices collect about themselves every 10 minutes. After collecting these statistics, each Viptela device places them into a zip file. The vManage server retrieves these zip files every 10 minutes or, if the vManage server cannot log in to the device, it retrieves them whenever it is next able to log in. Resource URL: /alarms,  /statistics , /event |
| Real-Time Monitoring	| Retrieving, viewing, and managing real-time statistics and traffic information. Real-time monitoring information is gathered in real time, approximately once per second. Resource URL: /device/app-route/statistics , /device/bfd/status |
| Troubleshooting | Tools	Troubleshooting devices, for determining the effect of policy, for updating software, and for retrieving software version information. Resource URL: /device/action/software , /device/tools/ping/|


In this lab, we will learn how to build a CLI application that leverages the vManage REST API's to retrieve data, parse it, extract pertinent information and display it to the user.

Let's start with login() function which is used to get authenticated with vManage and recieve cookie which is used for authentication in subsequenct API calls. 

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

# Device Inventory and Monitoring API's

### URL Structure Components

https://<vmanage-ip:port>/dataservice/device

|  |  |
| ------ | ------ |
| http:// or https://  | Protocol over which data is sent  between client and server |
| Server or Host  | Resolves to the IP and port to which to connect, example : "<vmanage-ip:port>" |
| Resource | The location of the data or object of  interest, example : "/device" |
| Parameters  | Details to scope, filter, or clarify a request. Often optional|

Example for Parameters
  -   URL : https://<vmanage-ip:port>/dataservice/device/bfd/state/device?deviceId=1.1.1.7 
  -   "?deviceId=1.1.1.7" is used to filter out bfd state for device with system-ip/deviceId = 1.1.1.7

Now let’s make an API call to fetch the list of devices in the SD-WAN fabric. Resource URI for this is "device".

Note:  All REST API calls to vmanage contains the root "/dataservice" , so URL to fetch devices is  "https://vmanage-ip:port/dataservice/device"

In `vmanage_apis.py` , we define a class `rest_api_lib` which has methods `login()`, `get_request()` and `post_request()`

After authentication is done with the vManage using `login()` function, we will run the `get_request` method of `rest_api_lib` class object to get a list of all the devices in the fabric and store the JSON data that is returned by the API in the response variable.

Now we extract just the `[data]` portion of the JSON and store it in a variable called items. The items variable at this point contains lot of information about all the devices in the fabric.

Run the command `./vmanage_apis.py` to see the list of available options. 

```
$ ./vmanage_apis.py
Usage: vmanage_apis.py [OPTIONS] COMMAND [ARGS]...

  Command line tool for deploying templates to CISCO SDWAN.

Options:
  --help  Show this message and exit.

Commands:
  attach            Attach a template with Cisco SDWAN.
  attached-devices  Retrieve and return devices associated to a template.
  control-status    Retrieve and return information about Control status of...
  detach            Detach a template with Cisco SDWAN.
  device-counters   Retrieve and return information about Device Counters
                    of...
  interface-status  Retrieve and return information about Interface status...
  list-devices      Retrieve and return information about network devices
                    in...
  system-status     Retrieve and return information about system status of...
  template-list     Retrieve and return templates list.
```

# List Devices
 
Run the command `./vmanage_apis.py list-devices` to retrieve the list of devices and print pertinent information in table format. 
  
See the below sample response which includes all the information retrieved for one such network device and also filtered information about all network devices. 
  
  
```
$./vmanage_apis.py list-devices
Retrieving the device list
https://sdwandemo.cisco.com:8443/dataservice/device

Device details retrieved for one network device

{'bfdSessions': '42',
 'bfdSessionsUp': 42,
 'board-serial': 'C2E5BDC6',
 'certificate-validity': 'Valid',
 'connectedVManages': ['"1.1.1.55"'],
 'controlConnections': '5',
 'device-groups': ['"No groups"'],
 'device-model': 'vedge-cloud',
 'device-os': 'next',
 'device-type': 'vedge',
 'deviceId': '1.1.2.5',
 'domain-id': '1',
 'host-name': 'AWS-Direct',
 'isDeviceGeoData': True,
 'lastupdated': 1552714222725,
 'latitude': '45.52',
 'layoutLevel': 4,
 'linux_cpu_count': '1',
 'local-system-ip': '1.1.2.5',
 'longitude': '-122.67',
 'max-controllers': '0',
 'model_sku': 'None',
 'ompPeers': '2',
 'personality': 'vedge',
 'platform': 'x86_64',
 'reachability': 'reachable',
 'site-id': '5',
 'state': 'green',
 'state_description': 'All daemons up',
 'status': 'normal',
 'statusOrder': 4,
 'system-ip': '1.1.2.5',
 'testbed_mode': True,
 'timezone': 'America/Los_Angeles',
 'total_cpu_count': '4',
 'uptime-date': 1552688880000,
 'uuid': 'ecb07387-fc76-43a6-bb77-50fd03d45a06',
 'validity': 'valid',
 'version': '18.4.1'}

list of all devices retrieved
╒════════════════════╤═══════════════╤═══════════╤════════════╤═════════════╤════════════════════════╤═══════════╤════════════════╤═════════════╕
│ Host-Name          │ Device Type   │   Site ID │   Latitude │   Longitude │ Certificate Validity   │ Version   │ Device Model   │ System IP   │
╞════════════════════╪═══════════════╪═══════════╪════════════╪═════════════╪════════════════════════╪═══════════╪════════════════╪═════════════╡
│ vmanage            │ vmanage       │        55 │      41.87 │      -87.62 │ Valid                  │ 18.4.1    │ vmanage        │ 1.1.1.55    │
├────────────────────┼───────────────┼───────────┼────────────┼─────────────┼────────────────────────┼───────────┼────────────────┼─────────────┤
│ vSmart1            │ vsmart        │        53 │      41.87 │      -87.62 │ Valid                  │ 18.4.1    │ vsmart         │ 1.1.1.53    │
├────────────────────┼───────────────┼───────────┼────────────┼─────────────┼────────────────────────┼───────────┼────────────────┼─────────────┤
│ vSmart2            │ vsmart        │        54 │      41.87 │      -87.62 │ Valid                  │ 18.4.1    │ vsmart         │ 1.1.1.54    │
├────────────────────┼───────────────┼───────────┼────────────┼─────────────┼────────────────────────┼───────────┼────────────────┼─────────────┤
│ vBond1             │ vbond         │        51 │      41.87 │      -87.62 │ Valid                  │ 18.4.1    │ vedge-cloud    │ 1.1.1.51    │
├────────────────────┼───────────────┼───────────┼────────────┼─────────────┼────────────────────────┼───────────┼────────────────┼─────────────┤
│ vBond2             │ vbond         │        52 │      41.87 │      -87.62 │ Valid                  │ 18.4.1    │ vedge-cloud    │ 1.1.1.52    │
├────────────────────┼───────────────┼───────────┼────────────┼─────────────┼────────────────────────┼───────────┼────────────────┼─────────────┤
│ AWS-Direct         │ vedge         │         5 │      45.52 │     -122.67 │ Valid                  │ 18.4.1    │ vedge-cloud    │ 1.1.2.5     │
├────────────────────┼───────────────┼───────────┼────────────┼─────────────┼────────────────────────┼───────────┼────────────────┼─────────────┤
│ AWS-Gateway-East   │ vedge         │        10 │      37.43 │      -78.65 │ Valid                  │ 18.4.1    │ vedge-cloud    │ 1.1.1.10    │
├────────────────────┼───────────────┼───────────┼────────────┼─────────────┼────────────────────────┼───────────┼────────────────┼─────────────┤
│ AWS-Gateway-East   │ vedge         │        11 │      37.43 │      -78.65 │ Valid                  │ 18.4.1    │ vedge-cloud    │ 1.1.1.11    │
├────────────────────┼───────────────┼───────────┼────────────┼─────────────┼────────────────────────┼───────────┼────────────────┼─────────────┤
│ Azure-Gateway-West │ vedge         │        14 │      36.74 │     -119.77 │ Valid                  │ 18.4.1    │ vedge-cloud    │ 1.1.1.14    │
├────────────────────┼───────────────┼───────────┼────────────┼─────────────┼────────────────────────┼───────────┼────────────────┼─────────────┤
│ Azure-Gateway-West │ vedge         │        15 │      36.74 │     -119.77 │ Valid                  │ 18.4.1    │ vedge-cloud    │ 1.1.1.15    │
├────────────────────┼───────────────┼───────────┼────────────┼─────────────┼────────────────────────┼───────────┼────────────────┼─────────────┤
│ DataCenter1a       │ vedge         │        20 │      40.71 │      -74    │ Valid                  │ 18.4.1    │ vedge-cloud    │ 1.1.2.200   │
├────────────────────┼───────────────┼───────────┼────────────┼─────────────┼────────────────────────┼───────────┼────────────────┼─────────────┤
│ DataCenter1b       │ vedge         │        20 │      40.71 │      -74    │ Valid                  │ 18.4.1    │ vedge-cloud    │ 1.1.2.201   │
├────────────────────┼───────────────┼───────────┼────────────┼─────────────┼────────────────────────┼───────────┼────────────────┼─────────────┤
│ DataCenter2a       │ vedge         │        21 │      37.77 │     -122.43 │ Valid                  │ 18.4.1    │ vedge-cloud    │ 1.1.2.210   │
├────────────────────┼───────────────┼───────────┼────────────┼─────────────┼────────────────────────┼───────────┼────────────────┼─────────────┤
│ DataCenter2b       │ vedge         │        21 │      37.77 │     -122.43 │ Valid                  │ 18.4.1    │ vedge-cloud    │ 1.1.2.211   │
├────────────────────┼───────────────┼───────────┼────────────┼─────────────┼────────────────────────┼───────────┼────────────────┼─────────────┤
│ RegionalHub        │ vedge         │        22 │      30.26 │      -97.74 │ Valid                  │ 18.4.1    │ vedge-cloud    │ 1.1.2.22    │
├────────────────────┼───────────────┼───────────┼────────────┼─────────────┼────────────────────────┼───────────┼────────────────┼─────────────┤
│ RemoteSite1        │ vedge         │         1 │      37.33 │     -121.88 │ Valid                  │ 18.4.1    │ vedge-cloud    │ 1.1.2.1     │
├────────────────────┼───────────────┼───────────┼────────────┼─────────────┼────────────────────────┼───────────┼────────────────┼─────────────┤
│ RemoteSite2a       │ vedge         │         2 │      46    │     -100.54 │ Valid                  │ 18.4.1    │ vedge-cloud    │ 1.1.2.2     │
├────────────────────┼───────────────┼───────────┼────────────┼─────────────┼────────────────────────┼───────────┼────────────────┼─────────────┤
│ RemoteSite2b       │ vedge         │         2 │      46    │     -100.54 │ Valid                  │ 18.4.1    │ vedge-cloud    │ 1.1.2.4     │
├────────────────────┼───────────────┼───────────┼────────────┼─────────────┼────────────────────────┼───────────┼────────────────┼─────────────┤
│ RemoteSite3-4K     │ vedge         │         3 │      39.74 │     -104.99 │ Valid                  │ 16.10.2   │ vedge-ISR-4331 │ 1.1.2.3     │
╘════════════════════╧═══════════════╧═══════════╧════════════╧═════════════╧════════════════════════╧═══════════╧════════════════╧═════════════╛
```

#	Control Status

To learn how to use particular option, use help command `./vmanage_apis.py control-status --help`  

In `control-status` option, we use resource URI `device/control/synced/connections?deviceId=<system-ip>` to fetch the status of control connections. 
    
```
  
$ ./vmanage_apis.py control-status --help
Usage: vmanage_apis.py control-status [OPTIONS]

  Retrieve and return information about Control status of network device in
  SD-WAN fabric

  Example command:     ./vmanage_apis.py interface_status

Options:
  --system_ip TEXT  System IP address of the device
  --help            Show this message and exit.
  
#cedge 
  
$ ./vmanage_apis.py control-status --system_ip 1.1.2.3
Retrieving the Control Status
https://sdwandemo.cisco.com:8443/dataservice/device/control/synced/connections?deviceId=1.1.2.3

Control Connection status for Device =  1.1.2.3
╒═════════════╤══════════════════╤═════════╤═════════════════════╕
│ Peer Type   │ Peer System IP   │ state   │ Last Updated        │
╞═════════════╪══════════════════╪═════════╪═════════════════════╡
│ vmanage     │ 1.1.1.55         │ up      │ 03/15/2019 22:39:11 │
├─────────────┼──────────────────┼─────────┼─────────────────────┤
│ vsmart      │ 1.1.1.53         │ up      │ 03/15/2019 22:39:11 │
├─────────────┼──────────────────┼─────────┼─────────────────────┤
│ vsmart      │ 1.1.1.54         │ up      │ 03/15/2019 22:39:11 │
╘═════════════╧══════════════════╧═════════╧═════════════════════╛

#vedge

$ ./vmanage_apis.py control-status --system_ip 1.1.2.4
Retrieving the Control Status
https://sdwandemo.cisco.com:8443/dataservice/device/control/synced/connections?deviceId=1.1.2.4

Control Connection status for Device =  1.1.2.4
╒═════════════╤══════════════════╤═════════╤═════════════════════╕
│ Peer Type   │ Peer System IP   │ state   │ Last Updated        │
╞═════════════╪══════════════════╪═════════╪═════════════════════╡
│ vsmart      │ 1.1.1.53         │ up      │ 03/16/2019 03:31:52 │
├─────────────┼──────────────────┼─────────┼─────────────────────┤
│ vsmart      │ 1.1.1.54         │ up      │ 03/16/2019 03:31:52 │
├─────────────┼──────────────────┼─────────┼─────────────────────┤
│ vmanage     │ 1.1.1.55         │ up      │ 03/16/2019 03:31:52 │
├─────────────┼──────────────────┼─────────┼─────────────────────┤
│ vsmart      │ 1.1.1.53         │ up      │ 03/15/2019 22:32:11 │
├─────────────┼──────────────────┼─────────┼─────────────────────┤
│ vsmart      │ 1.1.1.54         │ up      │ 03/15/2019 22:32:11 │
╘═════════════╧══════════════════╧═════════╧═════════════════════╛

```
# Interface Status

In `interface-status` option, we use resource URI `device/interface/synced?deviceId=<system-ip>` to fetch the interface status of one such network device in fabric.

```
#cedge

./vmanage_apis.py interface-status --system_ip 1.1.2.3
Retrieving the interface Status
https://sdwandemo.cisco.com:8443/dataservice/device/interface/synced?deviceId=1.1.2.3

Interfaces status for Device =  1.1.2.3
╒══════════════════════╤════════════════════════════════╕
│ Interface Name       │ Operational status             │
╞══════════════════════╪════════════════════════════════╡
│ GigabitEthernet0/0/0 │ if-oper-state-ready            │
├──────────────────────┼────────────────────────────────┤
│ GigabitEthernet0/0/1 │ if-oper-state-ready            │
├──────────────────────┼────────────────────────────────┤
│ GigabitEthernet0/0/2 │ if-oper-state-lower-layer-down │
├──────────────────────┼────────────────────────────────┤
│ GigabitEthernet0     │ if-oper-state-lower-layer-down │
├──────────────────────┼────────────────────────────────┤
│ Tunnel0              │ if-oper-state-ready            │
├──────────────────────┼────────────────────────────────┤
│ Control Plane        │ if-oper-state-ready            │
├──────────────────────┼────────────────────────────────┤
│ Loopback65528        │ if-oper-state-ready            │
├──────────────────────┼────────────────────────────────┤
│ VirtualPortGroup0    │ if-oper-state-ready            │
├──────────────────────┼────────────────────────────────┤
│ VirtualPortGroup1    │ if-oper-state-ready            │
├──────────────────────┼────────────────────────────────┤
│ Tunnel6000001        │ if-oper-state-ready            │
╘══════════════════════╧════════════════════════════════╛

#vedge 

$ ./vmanage_apis.py interface-status --system_ip 1.1.2.4
Retrieving the interface Status
https://sdwandemo.cisco.com:8443/dataservice/device/interface/synced?deviceId=1.1.2.4

Interfaces status for Device =  1.1.2.4
╒══════════════════╤══════════════════════╕
│ Interface Name   │ Operational status   │
╞══════════════════╪══════════════════════╡
│ ge0/0            │ Up                   │
├──────────────────┼──────────────────────┤
│ ge0/0            │ Up                   │
├──────────────────┼──────────────────────┤
│ ge0/1            │ Up                   │
├──────────────────┼──────────────────────┤
│ ge0/1            │ Up                   │
├──────────────────┼──────────────────────┤
│ ge0/2            │ Up                   │
├──────────────────┼──────────────────────┤
│ ge0/2            │ Up                   │
├──────────────────┼──────────────────────┤
│ system           │ Up                   │
├──────────────────┼──────────────────────┤
│ system           │ Up                   │
├──────────────────┼──────────────────────┤
│ loopback1        │ Up                   │
├──────────────────┼──────────────────────┤
│ loopback2        │ Up                   │
├──────────────────┼──────────────────────┤
│ eth0             │ Up                   │
╘══════════════════╧══════════════════════╛

```  

# Device Counters

In `device-counters` option, we use resource URI `device/counters?deviceId=<system-ip>` to fetch the OMP peers and BFD session status of one such network device in fabric.


```
#cedge

$ ./vmanage_apis.py device-counters --system_ip 1.1.2.3
Retrieving the Device Counters
https://sdwandemo.cisco.com:8443/dataservice/device/counters?deviceId=1.1.2.3

Device Counters for Device =  1.1.2.3
╒════════════════╤══════════════════╤══════════════════════╤═══════════════════╤═════════════════════╕
│   OMP Peers Up │   OMP Peers Down │   Vsmart connections │   BFD Sessions Up │   BFD Sessions Down │
╞════════════════╪══════════════════╪══════════════════════╪═══════════════════╪═════════════════════╡
│              2 │                0 │                    2 │                22 │                   0 │
╘════════════════╧══════════════════╧══════════════════════╧═══════════════════╧═════════════════════╛

#vedge

./vmanage_apis.py device-counters --system_ip 1.1.2.4
Retrieving the Device Counters
https://sdwandemo.cisco.com:8443/dataservice/device/counters?deviceId=1.1.2.4

Device Counters for Device =  1.1.2.4
╒════════════════╤══════════════════╤══════════════════════╤═══════════════════╤═════════════════════╕
│   OMP Peers Up │   OMP Peers Down │   Vsmart connections │   BFD Sessions Up │   BFD Sessions Down │
╞════════════════╪══════════════════╪══════════════════════╪═══════════════════╪═════════════════════╡
│              2 │                0 │                    4 │                38 │                   0 │
╘════════════════╧══════════════════╧══════════════════════╧═══════════════════╧═════════════════════╛
```

# System Status

In `system-status` option, we use resource URI `device/system/status?deviceId=<system-ip>` to fetch the system status of one such network device in fabric.

```
#cedge

$ ./vmanage_apis.py system-status --system_ip 1.1.2.3
Retrieving the System Status
https://sdwandemo.cisco.com:8443/dataservice/device/system/status?deviceId=1.1.2.3

System status for Device =  1.1.2.3
╒════════════════╤═════════════════════════════╤═══════════╤═══════════════╤══════════════╕
│ Host name      │ Up time                     │ Version   │   Memory Used │   CPU system │
╞════════════════╪═════════════════════════════╪═══════════╪═══════════════╪══════════════╡
│ RemoteSite3-4K │ 1 days 07 hrs 32 min 18 sec │ 16.10.2   │       4533804 │          5.8 │
╘════════════════╧═════════════════════════════╧═══════════╧═══════════════╧══════════════╛

#vedge

$ ./vmanage_apis.py system-status --system_ip 1.1.2.4
Retrieving the System Status
https://sdwandemo.cisco.com:8443/dataservice/device/system/status?deviceId=1.1.2.4

System status for Device =  1.1.2.4
╒══════════════╤═════════════════════════════╤═══════════╤═══════════════╤══════════════╕
│ Host name    │ Up time                     │ Version   │   Memory Used │   CPU system │
╞══════════════╪═════════════════════════════╪═══════════╪═══════════════╪══════════════╡
│ RemoteSite2b │ 1 days 07 hrs 35 min 16 sec │ 18.4.1    │       2147004 │         4.78 │
╘══════════════╧═════════════════════════════╧═══════════╧═══════════════╧══════════════╛
```
# Configuration API's


# Templates list

In `template-list` option, we use resource URI `template/device` to fetch the list of templates.

```

cedge and vedge template lists

$ ./vmanage_apis.py template-list
Retrieving the templates available.
https://sdwandemo.cisco.com:8443/dataservice/template/device
╒═════════════════════════════╤════════════════╤══════════════════════════════════════╤════════════════════╤════════════════════╕
│ Template Name               │ Device Type    │ Template ID                          │   Attached devices │   Template version │
╞═════════════════════════════╪════════════════╪══════════════════════════════════════╪════════════════════╪════════════════════╡
│ Remote-Sites-vEdge-Dual-Biz │ vedge-cloud    │ 049d8332-8d52-4a6b-a487-4807f58c52f5 │                  1 │                 16 │
├─────────────────────────────┼────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Remote-Sites-vEdge-Dual-Pub │ vedge-cloud    │ df0b0930-a85a-4dd7-9e4f-0c853c993c16 │                  1 │                 16 │
├─────────────────────────────┼────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Remote-Sites-vEdge-Single   │ vedge-cloud    │ 3b3cb89d-df49-4dde-9fcc-a1600874ff06 │                  1 │                 16 │
├─────────────────────────────┼────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Cloud-DataCenter            │ vedge-cloud    │ d1c53387-a166-4cc3-8993-970bd7dab975 │                  1 │                 15 │
├─────────────────────────────┼────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ DataCenters                 │ vedge-cloud    │ 4378a23b-4b23-45cd-b4cc-6a5ada722d37 │                  4 │                 16 │
├─────────────────────────────┼────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Remote-Sites-4K             │ vedge-ISR-4331 │ 78848213-14c1-4d1c-8481-043912893517 │                  1 │                 13 │
├─────────────────────────────┼────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Cloud-onRamp                │ vedge-cloud    │ afcf379b-b183-4bd6-86be-5428965f3168 │                  6 │                 13 │
├─────────────────────────────┼────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Regional-Hub                │ vedge-cloud    │ 85809554-daa4-4be9-b2d3-6c490c8d596d │                  1 │                 15 │
╘═════════════════════════════╧════════════════╧══════════════════════════════════════╧════════════════════╧════════════════════╛
$
```

# Create Templates

# URL Structure Components

https://<vmanage-ip:port>/dataservice/template/feature/

Now let’s start using the python script to create the template by using below steps

  - login and authenticate to a vManage instance
  - Build payload to provide the variables needed to create template
  - Perform the POST operation by sending template variables in payload. 

Once authentication is done, let’s define the payload which can be used to define the template.

We can use `.yaml` file to store all the required variables for configuring the template. For example, please see below file `banner_config.yaml`

```
$ cat banner_config.yaml
template_name: 'vedge_cloud_banner'
template_description: 'vedge_cloud_banner'
login_banner: 'test_yaml_banner_login'
motd_banner: 'test_yaml_banner_motd'
device_type: 'vedge-cloud'
```

While building the templates, we can load the content from above `.yaml` file 

```
with open(input_yaml) as f:
	config = yaml.safe_load(f.read())
```

`.yaml` file contents are stored in `config` dictionary which is used in creating below payload variable. 

```
payload = {
    "templateName": config["template_name"],
    "templateMinVersion": "15.0.0",
    "templateDescription": config["template_description"],
    "templateType": "banner",
    "templateDefinition": {
        "login": {
            "vipObjectType": "object",
            "vipType": "constant",
            "vipValue": config["login_banner"],  # using the values defined for login banner in yaml file
            "vipVariableName": "banner_login"
        },
        "motd": {
            "vipObjectType": "object",
            "vipType": "constant",
            "vipValue": config["motd_banner"],  # using the values defined for motd banner in yaml file
            "vipVariableName": "banner_motd"
        }
    },
    "deviceType": [
        config["device_type"]
    ],
    "deviceModels": [
        {
            "name": "vedge-cloud",
            "displayName": "vEdge Cloud",
            "deviceType": "vedge",
            "isCliSupported": True,
            "isCiscoDeviceModel": False
        }
    ],
    "factoryDefault": False
    }
```

code snip to do POST request to URL "template/feature/" to create the template. 

```
response = vmanage_session.post_request('template/feature/', payload)
if response.status_code == 200:
	print("\nCreated banner template ID: ", response.json())
else:
   print("\nFailed creating banner template, error: ",response.text)
```

Provide the yaml file to script using the option `--input_yaml`

```
$ ./vmanage_apis.py create-feature-template --input_yaml banner_config.yaml
Creating feature template based on yaml file details
Loading Network Configuration Details from YAML File

Created banner template ID:  {'templateId': '493667fb-635f-49f4-bd83-9b430497be26'}
```

When template is created, the vManage returns the templateId which can be used in further operations like attaching the feature template to the device template. 


complete script can be accessed [here](https://github.com/suchandanreddy/sdwan-apis/blob/master/restapi.py)

# DPI statistics

The query collects statistics for the 2 days between 2/15 - 2/17, for the system IP address 1.1.2.1,
and for application families web, instant-messaging, network-management, network-service, 
application-service and webmail. 

The aggregation portion of the query determines how data is bucketized/grouped. 

Here, the statistics are aggregated in 6 hour intervals, and for each application family, they contain the total 
number (sum) of data octets. 

The output is returned in a json array. The comments in the aggregation portion of the example indicate the 
order in which the bucketization occurs.


#Firewall Monitoring API's

Using monitoring API's we can retrieve status, statistics, alarms and other details about devices in SD-WAN Fabric. 

Resource URL's: /alarms,  /statistics , /event etc. 

#URL Structure Components

In order to retrieve firewall statistics i.e. inspect count, drop count we need to use the resource URL "/statistics/fwall/aggregation"

URL : https://<vmanage-ip:port>/dataservice/statistics/fwall/aggregation

| Component  | Description  |
| ------ | ------ |
| http:// or https://  | Protocol over which data is sent  between client and server |
| Server or Host  | Resolves to the IP and port to which to connect, example : "<vmanage-ip:port>" |
| Resource | The location of the data or object of  interest, example : "statistics/fwall/aggregation" |

Now let’s start using the python script to fetch the firewall inspect and drop count by using below steps

  - login and authenticate to a vManage instance
  - Build Query to specify the rules and how to collect firewall statistics. 
  - Perform the POST operation by sending query in payload

Using `login()` funtion in `rest_api_lib` we will authenticate with vManage and get cookie or JSESSIONID which is to be used in further API calls. 

In order to retrieve the firewall statistics we need to send Query which describes how statistics should be aggregated. 

Now let’s define the Query which can be used to collect firewall statistics using POST operation on Resource URL "/dataservice/statistics/fwall/aggregation"

#Query Payload

#Example-1

-	Below example query retrieves firewall inspect count values for last 24 hours from all network devices in fabric.

-	The aggregation portion of the query determines how data is bucketized/grouped. 

-	Here, the statistics are aggregated in 30 mins intervals across the span of 24 hours. 

-	The output is returned in a json array. 

```
{
"aggregation": {			                # Defines how statistics are bucketized  
"metrics": [
      {
        "property": "fw_total_insp_count",  # Bucketized based on property for example   
        "type": "sum",                        firewall total inspect packet count
        "order": "desc"
      }
    ],
    "histogram": {.                         # Time interval is 30 mins
      "property": "entry_time",
      "type": "minute",
      "interval": 30,
      "order": "asc"
    }
  },
  "query": {
    "condition": "AND",         # Aggregated data must match both the rules specified below
    "rules": [
      {
        "value": [
          "24"				                Rule #1: Statistics from the last 24 hours
        ],
        "field": "entry_time",
        "type": "date",
        "operator": "last_n_hours"
      },
      {
        "value": [
          "total"			                Rule #2: Total packets count for firewall inspect
        ],
        "field": "type",
        "type": "string",
        "operator": "in"
      }
    ]
  }
}

```

# Example-2

-	Below query retrieves the firewall Drop count for last 24 hours. 

```
{
  "aggregation": {
    "metrics": [
      {
        "property": "fw_total_drop_count",
        "type": "sum",
        "order": "desc"
      }
    ],
    "histogram": {
      "property": "entry_time",
      "type": "minute",
      "interval": 30,
      "order": "asc"
    }
  },
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
          "total"
        ],
        "field": "type",
        "type": "string",
        "operator": "in"
      }
    ]
  }
}
```

# Example-3

-	Below query retrieves the firewall Inspect count for last 1 hour and aggregated for 1 minute intervals.

```
{
  "aggregation": {
    "metrics": [
      {
        "property": "fw_total_insp_count",
        "type": "sum",
        "order": "desc"
      }
    ],
    "histogram": {
      "property": "entry_time",
      "type": "minute",
      "interval": 1,
      "order": "asc"
    }
  },
  "query": {
    "condition": "AND",
    "rules": [
      {
        "value": [
          "1"
        ],
        "field": "entry_time",
        "type": "date",
        "operator": "last_n_hours"
      },
      {
        "value": [
          "total"
        ],
        "field": "type",
        "type": "string",
        "operator": "in"
      }
    ]
  }
}
```

Using the query lets perform POST operation on URI to retrieve the firewall inspect count statistics for last 24 hours in intervals of 30 mins. 

# POST Operation

To fetch the ZBF inspect packet count or drop count we need to perform POST operation.

Input parameters for POST operation

-   endpoint (vmanage server ip address)
-   resource or mountpoint represented by the URL
-   headers (Content-type and Accept are set to application/json)
-   The query which defines how firewall statistics are collected is sent using the payload. 

"verify=False" parameter is passed in POST operation because the SSL verification is disabled.

The result of the POST operation is stored in the response variable. The json() method is called on the response object and the JSON format of the response is returned. "data" key in the JSON output contains the entry_time and inspect/drop count associated in dictionary format. 

```
def post_request(self, mount_point, payload, headers={'Content-type': 'application/json', 'Accept': 'application/json'}):

        """POST request"""
        url = "https://%s:%s/dataservice/%s"%(self.vmanage_host, self.vmanage_port, mount_point)
        payload = json.dumps(payload)
        response = self.session[self.vmanage_host].post(url=url, data=payload, headers=headers, a)
        return response
```

Now let's have a look at the response to POST operation

# Sample Response

```
$ python zbfw_api.py

Firewall Inspect count

  "data": [
    {
      "entry_time": 1552807800000,
      "count": 92,
      "fw_total_insp_count": 278
    },
    {
      "entry_time": 1552806000000,
      "count": 360,
      "fw_total_insp_count": 1050
    },
    {
      "entry_time": 1552804200000,
      "count": 360,
      "fw_total_insp_count": 1052
    },
    {
      "entry_time": 1552802400000,
      "count": 360,
      "fw_total_insp_count": 1051
    },
<snip>  
```

"entry_time" values are in epoch format. Use time function in python to convert epoch values to format MM-DD-YYYY HH-MM-SS format

For example 

```
>>> entry_time = 1552309200000
>>> time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(entry_time/1000.))
'03/11/2019 13:00:00'
>>>

```

Now let's store these firewall inspect count values in a Time Series Database (TSDB) Influx DB and plot it on to Grafana Dashboard

# Influx DB:

 -	InfluxDB is an open-source time series database which is optimized for fast, high-availability storage and retrieval of time series data in fields such as operations monitoring, application metrics, Internet of Things sensor data, and real-time analytics. It provides a SQL-like language with built-in time functions for querying a data structure composed of measurements, series, and points
 
-	Grafana (Application): an open-source platform to build monitoring and analytics dashboards. 

Here, we are using InfluxDB as a datasource for Grafana to plot the information on dashboard. 

# Prerequisites

Install influxdb and grafana on Ubuntu


# Install InfluxDB

For installing influxdb on ubuntu, please check [here](https://docs.influxdata.com/influxdb/v0.12/introduction/installation/)

Below are the commands to install influxdb.

```
apt-get update

curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -

source /etc/lsb-release

echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

apt-get update && sudo apt-get install influxdb

service influxdb start
```

# Installation Logs

```
root@ubuntu:~# apt-get update

root@ubuntu:~# curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
OK
root@ubuntu:~# 

root@ubuntu:~# source /etc/lsb-release

root@ubuntu:~# echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

deb https://repos.influxdata.com/ubuntu xenial stable

root@ubuntu:~# apt-get update && sudo apt-get install influxdb
Hit:1 https://repos.influxdata.com/ubuntu xenial InRelease
Hit:2 http://us.archive.ubuntu.com/ubuntu xenial InRelease                               
Get:3 http://security.ubuntu.com/ubuntu xenial-security InRelease [109 kB]
Get:4 http://us.archive.ubuntu.com/ubuntu xenial-updates InRelease [109 kB]
Get:5 http://us.archive.ubuntu.com/ubuntu xenial-backports InRelease [107 kB]
Fetched 325 kB in 2s (139 kB/s)   
Reading package lists... Done
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following packages were automatically installed and are no longer required:
  gnome-software-common libgtkspell3-3-0
Use 'sudo apt autoremove' to remove them.
The following NEW packages will be installed:
  influxdb
0 upgraded, 1 newly installed, 0 to remove and 694 not upgraded.
Need to get 46.7 MB of archives.
After this operation, 107 MB of additional disk space will be used.
Get:1 https://repos.influxdata.com/ubuntu xenial/stable amd64 influxdb amd64 1.7.4-1 [46.7 MB]
Fetched 46.7 MB in 1s (26.1 MB/s)   
Selecting previously unselected package influxdb.
(Reading database ... 172371 files and directories currently installed.)
Preparing to unpack .../influxdb_1.7.4-1_amd64.deb ...
Unpacking influxdb (1.7.4-1) ...
Processing triggers for man-db (2.7.5-1) ...
Setting up influxdb (1.7.4-1) ...
Created symlink from /etc/systemd/system/influxd.service to /lib/systemd/system/influxdb.service.
Created symlink from /etc/systemd/system/multi-user.target.wants/influxdb.service to /lib/systemd/system/influxdb.service.
root@ubuntu:~# 
root@ubuntu:~#service influxdb start
```

#	Connect to InfluxDB

-	Run command influx and create database to store firewall inspect count values

```
root@ubuntu:~# influx
Connected to http://localhost:8086 version 1.7.4
InfluxDB shell version: 1.7.4
Enter an InfluxQL query
> 
```

-	Create a `firewall_inspect` database using the command `CREATE DATABASE firewall_inspect` 

-	Create command doesn't produce any output, but when we run `SHOW DATABASES` command we can see it in the list

```
> SHOW DATABASES
name: databases
name
----
_internal
firewall_inspect
```

-	Select the database using command `USE firewall_inspect`

```
> USE firewall_inspect
Using database firewall_inspect
> 
```

-	Insert some test data using the following command.

```
INSERT firewall_inspect_count,host=wan_edge value=1021
```

-	Insert command does not produce any output, we can see the data when we perform a query using the below command

```
SELECT * from firewall_inspect_count
```

```
> SELECT * from firewall_inspect_count
name: firewall_inspect_count
time                host     value
----                ----     -----
1552830488724501604 wan_edge 1021
> 
```

-	In order to populate the Influx DB using the firewall inspect count values retrieved from API call, we use the python package influxdb to initiate client connection and store the time series data. 

-	Install the influxdb package using pip3

```
pip3 install influxdb
```

-	code snip to write the retrieved firewall inspect count values into Influx DB (firewall_inspect)

```
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

```

Now let's install Grafana and plot these firewall inspect count values on a dashboard 

# Install Grafana

Below instructions are based on the official documentation, available [here](http://docs.grafana.org/installation/debian/)

```
echo "deb https://packagecloud.io/grafana/testing/debian/ wheezy main" | sudo tee /etc/apt/sources.list.d/grafana.list

curl https://packagecloud.io/gpg.key | sudo apt-key add -

apt-get update && sudo apt-get install grafana

service grafana-server start

```

# Installation Logs

```
root@ubuntu:~# echo "deb https://packagecloud.io/grafana/testing/debian/ wheezy main" | sudo tee /etc/apt/sources.list.d/grafana.list
deb https://packagecloud.io/grafana/testing/debian/ wheezy main
root@ubuntu:~# 

root@ubuntu:~# curl https://packagecloud.io/gpg.key | sudo apt-key add -
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  3102  100  3102    0     0   1747      0  0:00:01  0:00:01 --:--:--  1747
OK
root@ubuntu:~# 

root@ubuntu:~# apt-get update && sudo apt-get install grafana
Hit:1 https://repos.influxdata.com/ubuntu xenial InRelease
Get:2 http://security.ubuntu.com/ubuntu xenial-security InRelease [109 kB]
Hit:3 http://us.archive.ubuntu.com/ubuntu xenial InRelease
Get:4 http://us.archive.ubuntu.com/ubuntu xenial-updates InRelease [109 kB]       
Get:5 https://packagecloud.io/grafana/testing/debian wheezy InRelease [23.4 kB]
Ign:5 https://packagecloud.io/grafana/testing/debian wheezy InRelease
Get:6 https://packagecloud.io/grafana/testing/debian wheezy/main amd64 Packages [15.7 kB]
Get:7 http://us.archive.ubuntu.com/ubuntu xenial-backports InRelease [107 kB]
Get:8 https://packagecloud.io/grafana/testing/debian wheezy/main i386 Packages [14 B]
Fetched 364 kB in 3s (96.2 kB/s)
Reading package lists... Done
W: GPG error: https://packagecloud.io/grafana/testing/debian wheezy InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 285D5812F5A66BFE
W: The repository 'https://packagecloud.io/grafana/testing/debian wheezy InRelease' is not signed.
N: Data from such a repository can't be authenticated and is therefore potentially dangerous to use.
N: See apt-secure(8) manpage for repository creation and user configuration details.
W: There is no public key available for the following key IDs:
285D5812F5A66BFE  
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following packages were automatically installed and are no longer required:
  gnome-software-common libgtkspell3-3-0
Use 'sudo apt autoremove' to remove them.
The following NEW packages will be installed:
  grafana
0 upgraded, 1 newly installed, 0 to remove and 694 not upgraded.
Need to get 55.4 MB of archives.
After this operation, 159 MB of additional disk space will be used.
WARNING: The following packages cannot be authenticated!
  grafana
Install these packages without verification? [y/N] y
Get:1 https://packagecloud.io/grafana/testing/debian wheezy/main amd64 grafana amd64 5.4.2 [55.4 MB]
Fetched 55.4 MB in 4s (11.5 MB/s)  
Selecting previously unselected package grafana.
(Reading database ... 172397 files and directories currently installed.)
Preparing to unpack .../grafana_5.4.2_amd64.deb ...
Unpacking grafana (5.4.2) ...
Processing triggers for ureadahead (0.100.0-19) ...
Processing triggers for systemd (229-4ubuntu4) ...
Setting up grafana (5.4.2) ...
Adding system user `grafana' (UID 121) ...
Adding new user `grafana' (UID 121) with group `grafana' ...
Not creating home directory `/usr/share/grafana'.
### NOT starting on installation, please execute the following statements to configure grafana to start automatically using systemd
 sudo /bin/systemctl daemon-reload
 sudo /bin/systemctl enable grafana-server
### You can start grafana-server by executing
 sudo /bin/systemctl start grafana-server
Processing triggers for ureadahead (0.100.0-19) ...
Processing triggers for systemd (229-4ubuntu4) ...
root@ubuntu:~# 

root@ubuntu:~# service grafana-server start
root@ubuntu:~# 

```

# Configure Grafana

Note: Below screenshots are for Grafana version 5.4.2

```
root@ubuntu:~# grafana-cli --version
Grafana cli version 5.4.2
root@ubuntu:~# 
```

-	Use web browser and login to Grafana at http://localhost:3000/  (Username/Password:admin/admin) . After login, we see below home screen.

![homescreen](Grafana_homescreen.png)

-	select Add Data Sources and select Influx DB. 

![datasource](datasource_1.png)

-	Provide Influx DB details i.e. URL, username, password and Database name.

![datasource](datasource_2.png)

-	Select Save and Test option and check if Data source is working.

![datasource](datasource_3.png)


# Create a Dashboard

-	Now let's create Dashboard by selecting New dashboard option

![Dashboard](dashboard_1.png)

-	Select graph panel and edit Panel title to select the Influx DB as a data source and define Query to retreive the values from database. In our case we have to query `firewall_inspect_count` values from Influx DB.
 
![Dashboard](dashboard_3.png)

-	Now Grafana sends query to influx DB and plots the graph on Dashboard as seen below.

![Dashboard](dasboard_final_2.png)

-	Above graph corresponds to this plot on vmanage

![vmanage](vmanage_screen.png)

Complete script can be accessed [here]()

## Notes for mac

Install grafana and influxdb on Mac

```
brew install grafana

brew tap homebrew/services

brew services start grafana 

grafana-cli plugins install grafana-simple-json-datasource

brew install influxdb
```



# Webhook 

-   Webhooks enable push-model mechanism to send notifications in real-time.
-   In order to retrieve alarms in real-time from the vManage using the REST API's, we need to poll for the data frequently. However by using webhooks, vManage can send HTTP POST request to the external systems in real-time once alarm is received. 
-   Webhooks are sometimes referred to as “Reverse APIs,” and we must design an API to consume or process the data sent via webhook.

# Prerequisites

-  This feature is supported from vManage 18.3 release onwards

# Configure

Steps to enable webhook notifications for pushing alarms to external systems.

-    Select "Email Notifications" from "Monitor -> Alarms" 
-    Enable webhook checkbox. 
-    Select severity level and Alarms for which webhook notifications should be triggered.
-    Provide the webhook server URL, username and password for webhook. ( Note : If webhook server doesn't have authentication configured, please provide dummy username and password )
-    Webhook URL can be http:// or https://

Note: provide the dummy email address as place holder for Email notifications and then click Add.

Below is an example screenshot, Here we are enabling webhook notifications for Critical and Medium alarms related to *"interface-admin-state-change"* and *"interface-state-change"*

![webhook](webhook_create_4.png)

Notifications can be enabled for all devices or custom list of devices. 

![webhook](webhook_create_3.png)

#	Notifications Dashboard 

![webhook](webhook_create_2.png)

# Test Webhook

From vManage shell, run curl command and send dummy HTTP POST request to webhook server to make sure it is reachable.

Sample output (using webhook.site as server)

```
vmanage:~$ curl -v -X POST -H 'Content-type: application/json' https://webhook.site/cb208ecc-4520-4bcd-b4b3-28f58d7b129d
*   Trying 188.226.137.35...
* TCP_NODELAY set
* Connected to webhook.site (188.226.137.35) port 443 (#0)
* found 157 certificates in /etc/ssl/certs/ca-certificates.crt
* ALPN, offering http/1.1
* SSL connection using TLS1.2 / ECDHE_RSA_AES_256_GCM_SHA384
* 	 server certificate verification OK
* 	 server certificate status verification SKIPPED
* 	 common name: webhook.site (matched)
* 	 server certificate expiration date OK
* 	 server certificate activation date OK
* 	 certificate public key: RSA
* 	 certificate version: #3
* 	 subject: CN=webhook.site
* 	 start date: Mon, 17 Dec 2018 11:32:42 GMT
* 	 expire date: Sun, 17 Mar 2019 11:32:42 GMT
* 	 issuer: C=US,O=Let's Encrypt,CN=Let's Encrypt Authority X3
* 	 compression: NULL
* ALPN, server did not agree to a protocol
> POST /cb208ecc-4520-4bcd-b4b3-28f58d7b129d HTTP/1.1
> Host: webhook.site
> User-Agent: curl/7.58.0
> Accept: */*
> Content-type: application/json
>
< HTTP/1.1 200 OK
< Server: nginx/1.10.3
< Content-Type: text/plain; charset=UTF-8
< Transfer-Encoding: chunked
< Vary: Accept-Encoding
< X-Request-Id: fbcad435-4164-440b-a4de-0d82efa2fb41
< X-Token-Id: cb208ecc-4520-4bcd-b4b3-28f58d7b129d
< Cache-Control: no-cache, private
< Date: Sat, 16 Mar 2019 12:33:05 GMT
< X-RateLimit-Limit: 30
< X-RateLimit-Remaining: 29
<
* Connection #0 to host webhook.site left intact
vmanage:~$
```

# Set up Webhook server on ubuntu

Now let’s try to set up webhook server on ubuntu to accept notifications sent from vManage

- In order to accept HTTP post requests sent from vManage, we need to enable http web server and design API route.
- Below code spins up flask web server listening on port 5001 for HTTP POST request
- Defined alarms() functions accepts the POST request at route http://<server-ip>:<port>/ and extracts the data from request.

```
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/',methods=['POST'])
def alarms():
   data = json.loads(request.data)
   print(data)
   return "OK"

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001, debug=True)
```

# Logs from Webhook Server:

Spin up http webhook server as background process

```
$python3 webhook.py &
[1] 7889

 * Serving Flask app "webhook" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5001/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 216-076-679
```

Sample output on webhook server on receiving notifications from the vManage.

```
 {'devices': [{'system-ip': '1.1.1.2'}], 'eventname': 'interface-admin-state-change', 'type': 'interface-admin-state-change', 'rulename': 'interface-admin-state-change', 'component': 'VPN', 'entry_time': 1552699205000, 'statcycletime': 1552699205000, 'message': 'The interface admin-state changed to down', 'severity': 'Critical', 'severity_number': 1, 'uuid': '735d1df8-acba-47d6-94c1-a76fe6f7b12e', 'values': [{'host-name': 'vmanage', 'system-ip': '1.1.1.2', 'if-name': 'eth0', 'new-admin-state': 'down', 'vpn-id': '0'}], 'rule_name_display': 'Interface_Admin_State_Change', 'receive_time': 1552699205615, 'values_short_display': [{'host-name': 'vmanage', 'system-ip': '1.1.1.2', 'if-name': 'eth0', 'new-admin-state': 'down'}], 'acknowledged': False, 'active': True}
<vmanage-ip> - - [16/Mar/2019 01:22:14] "POST / HTTP/1.1" 200 -
{'devices': [{'system-ip': '1.1.1.2'}], 'eventname': 'interface-state-change', 'type': 'interface-state-change', 'rulename': 'interface-state-change', 'component': 'VPN', 'entry_time': 1552699205000, 'statcycletime': 1552699205000, 'message': 'The interface oper-state changed to down', 'severity': 'Critical', 'severity_number': 1, 'uuid': 'caffbef4-3ab2-49bc-b9e9-1d8e79753d2b', 'values': [{'host-name': 'vmanage', 'system-ip': '1.1.1.2', 'if-name': 'eth0', 'new-state': 'down', 'vpn-id': '0'}], 'rule_name_display': 'Interface_State_Change', 'receive_time': 1552699205815, 'values_short_display': [{'host-name': 'vmanage', 'system-ip': '1.1.1.2', 'if-name': 'eth0', 'new-state': 'down'}], 'acknowledged': False, 'active': True}
<vmanage-ip> - - [16/Mar/2019 01:22:14] "POST / HTTP/1.1" 200 -
{'devices': [{'system-ip': '1.1.1.2'}], 'eventname': 'interface-admin-state-change', 'type': 'interface-admin-state-change', 'rulename': 'interface-admin-state-change', 'component': 'VPN', 'entry_time': 1552699209000, 'statcycletime': 1552699209000, 'message': 'The interface admin-state changed to up', 'severity': 'Medium', 'severity_number': 3, 'uuid': 'b1785534-8132-4039-8472-d64e04d4e558', 'values': [{'host-name': 'vmanage', 'system-ip': '1.1.1.2', 'if-name': 'eth0', 'new-admin-state': 'up', 'vpn-id': '0'}], 'rule_name_display': 'Interface_Admin_State_Change', 'receive_time': 1552699209618, 'values_short_display': [{'host-name': 'vmanage', 'system-ip': '1.1.1.2', 'if-name': 'eth0', 'new-admin-state': 'up'}], 'acknowledged': False, 'cleared_events': ['735d1df8-acba-47d6-94c1-a76fe6f7b12e'], 'active': False}
<vmanage-ip> - - [16/Mar/2019 01:22:18] "POST / HTTP/1.1" 200 -
{'devices': [{'system-ip': '1.1.1.2'}], 'eventname': 'interface-state-change', 'type': 'interface-state-change', 'rulename': 'interface-state-change', 'component': 'VPN', 'entry_time': 1552699209000, 'statcycletime': 1552699209000, 'message': 'The interface oper-state changed to up', 'severity': 'Medium', 'severity_number': 3, 'uuid': '2ca8864f-8a94-4620-9b7a-716fa506e860', 'values': [{'host-name': 'vmanage', 'system-ip': '1.1.1.2', 'if-name': 'eth0', 'new-state': 'up', 'vpn-id': '0'}], 'rule_name_display': 'Interface_State_Change', 'receive_time': 1552699209818, 'values_short_display': [{'host-name': 'vmanage', 'system-ip': '1.1.1.2', 'if-name': 'eth0', 'new-state': 'up'}], 'acknowledged': False, 'cleared_events': ['caffbef4-3ab2-49bc-b9e9-1d8e79753d2b'], 'active': False}
<vmanage-ip> - - [16/Mar/2019 01:22:18] "POST / HTTP/1.1" 200 -
```

# Alarms on vManage

-	Above webhook logs corresponds to these alarms which were recieved by vManage.

![alarms](alarms.png)

# References

online webhooks can be set up using https://webhook.site

sdwan docs : https://sdwan-docs.cisco.com/Product_Documentation/vManage_How-Tos/Operation/Configure_Email_Notifications_for_Alarms



# Alarms API’s

  - REpresentational State Transfer (REST) is an architecture style for designing web-services applications
  - REST architecture uses a stateless, client–server, cacheable communications protocol.
  - The vManage web server uses HTTP and its secure counterpart, HTTPS, as the communications protocol
  - vManage API Documentation is built-in at https://<vmanage-ip:port>/apidocs
  - Test API calls can be tried out from swagger UI at /apidocs
  
# URL Structure Components

https://<vmanage-ip:port>/dataservice/alarms 

|  |  |
| ------ | ------ |
| http:// or https://  | Protocol over which data is sent  between client and server |
| Server or Host  | Resolves to the IP and port to which to connect, example : "<vmanage-ip:port>" |
| Resource | The location of the data or object of  interest, example : "dataservice/alarms" |


Now let’s start using the python script to fetch the alarms by using below steps

  - login and authenticate to a vManage instance
  - Build Query to specify the rules and how to collect alarms
  - Perform the POST operation by sending query in payload

Using `login()` funtion in `rest_api_lib` we will authenticate with vManage and get cookie or JSESSIONID which is to be used in further API calls. 

Now let’s define the Query which can be used to collect alarms using POST operation on "dataservice/alarms"

#   Query Payload

#   Example-1

-	Between operator can be used to fetch the alarms for a custom interval for example i.e. 4:51:00 UTC to 4:57:00 UTC ( 6 mins interval )

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

-	Collect only cleared Medium, Critical alarms between 4:57 and 4:58

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

-	Collect *Active* Critical, Major, Medium, Minor alarms related to "Pseudo Commit Status" between 20:00 and 21:00

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

Using these queries lets perform POST operation on resource URI to retrieve the alarms.

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

Response which has both Active and Cleared alarms , alarms can be correlated further based on uuid value. For example we can see alarm with uuid "36af5221-d248-4aef-bed6-0f9a59b30f98" is a cleared event which indicates *"The interface oper-state changed to up"* , The alarm that got cleared is provided by list of uuids in *cleared_events* : 9f75552d-4a2b-4085-9dcc-fd15148cf078

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

`entry_time`, `cleared_time` values are in epoch format.

Use time function to convert epoch values to format MM-DD-YYYY HH-MM-SS format

```
>>> entry_time = 1552309200000
>>> time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(entry_time/1000.))
'03/11/2019 13:00:00'
>>>
```

Complete script can be accessed [here](https://github.com/suchandanreddy/sdwan-apis/blob/master/alarms_api.py)
