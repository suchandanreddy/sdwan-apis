This article covers the API responses formats for various features in SD-WAN Security. 

In order to fetch the above events from the vManage using the REST APIs, we need to send POST request to resource URL : `https://<vmanage-ip>/dataservice/event` , with below query format which filters for IPS alerts for last 24 hours using the value "utd-ips-alert"

 
```
{
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
          "utd-ips-alert"  
        ],
        "field": "eventname",
        "type": "string",
        "operator": "in"
      }
    ]
  },
  "size": 10000
}
``` 

Sample JSON Response for one IPS alert message:

 
```
{
      "system_ip": "1.1.1.5",
      "vmanage_system_ip": "1.1.1.5",
      "tenant": "default",
      "device_type": "vedge",
      "entry_time": 1557256910000,
      "statcycletime": 1557256910000,
      "eventname": "utd-ips-alert",
      "component": "Software",
      "severity_level": "critical",
      "host_name": "BR1-CSR1000v",
      "event": "{\"utd-ips-alert\":{\"src-ip\":\"192.168.60.2\",\"dst-ip\":\"208.67.220.220\",\"rev\":2,\"gid\":1,\"src-port\":58501,\"system-ip\":\"1.1.1.5\",\"dst-port\":53,\"host-name\":\"BR1-CSR1000v\",\"vrf\":10,\"classification\":\"utd-ips-alert-classification-misc-activity\",\"message\":\"APP-DETECT DNS request for Dynamic Internet Technology domain dfgvx.com\",\"priority\":\"utd-ips-alert-priority-crit\",\"severity-level\":\"critical\",\"sid\":27984,\"xmlns\":\"http://cisco.com/ns/yang/Cisco-IOS-XE-ios-events-oper\",\"protocol\":17,\"action\":\"utd-ips-alert-action-drop\",\"timestamp\":\"2019-05-07T19:21:50.622437+00:00\"}}",
      "details": "host-name=BR1-CSR1000v; timestamp=2019-05-07T19:21:50.622437+00:00; action=utd-ips-alert-action-drop; sid=27984; gid=1; rev=2; classification=utd-ips-alert-classification-misc-activity; message=APP-DETECT DNS request for Dynamic Internet Technology domain dfgvx.com; priority=utd-ips-alert-priority-crit; src-ip=192.168.60.2; dst-ip=208.67.220.220; src-port=58501; dst-port=53; protocol=17; vrf=10",
      "id": "AWqTvrvB-NUUAWONJp68"
}
```

Command "show utd engine standard logging events" can be used to fetch IPS alert logs on XE-SDWAN CLI 

 
```
BR1-CSR1000v#show utd engine standard logging events | i APP

2019/05/07-06:16:53.727336 UTC [**] [Hostname: 1.1.1.5] [**] [Instance_ID: 1] [**] Drop [**] [1:27984:2] APP-DETECT DNS request for Dynamic Internet Technology domain dfgvx.com [**] [Classification: Misc activity] [Priority: 3] [VRF: 10] {UDP} 192.168.60.2:52733 -> 8.8.8.8:53
2019/05/07-06:17:56.865524 UTC [**] [Hostname: 1.1.1.5] [**] [Instance_ID: 1] [**] Drop [**] [1:27984:2] APP-DETECT DNS request for Dynamic Internet Technology domain dfgvx.com [**] [Classification: Misc activity] [Priority: 3] [VRF: 10] {UDP} 192.168.60.2:42210 -> 8.8.8.8:53
2019/05/07-06:18:11.873872 UTC [**] [Hostname: 1.1.1.5] [**] [Instance_ID: 1] [**] Drop [**] [1:27984:2] APP-DETECT DNS request for Dynamic Internet Technology domain dfgvx.com [**] [Classification: Misc activity] [Priority: 3] [VRF: 10] {UDP} 192.168.60.2:53032 -> 8.8.8.8:53
2019/05/07-06:18:26.882482 UTC [**] [Hostname: 1.1.1.5] [**] [Instance_ID: 1] [**] Drop [**] [1:27984:2] APP-DETECT DNS request for Dynamic Internet Technology domain dfgvx.com [**] [Classification: Misc activity] [Priority: 3] [VRF: 10] {UDP} 192.168.60.2:56496 -> 8.8.8.8:53
2019/05/07-18:20:28.241429 UTC [**] [Hostname: 1.1.1.5] [**] [Instance_ID: 1] [**] Drop [**] [1:46807:3] MALWARE-OTHER DNS request for known malware domain toknowall.com - Unix.Troja n.Vpnfilter [**] [Classification: A Network Trojan was Detected] [Priority: 1] [VRF: 10] {UDP} 192.168.60.2:44810 -> 208.67.220.220:53
2019/05/07-19:01:47.307739 UTC [**] [Hostname: 1.1.1.5] [**] [Instance_ID: 1] [**] Drop [**] [1:27984:2] APP-DETECT DNS request for Dynamic Internet Technology domain dfgvx.com [**]  [Classification: Misc activity] [Priority: 3] [VRF: 10] {UDP} 192.168.60.2:48517 -> 208.67.220.220:53
2019/05/07-19:01:52.318452 UTC [**] [Hostname: 1.1.1.5] [**] [Instance_ID: 1] [**] Drop [**] [1:27984:2] APP-DETECT DNS request for Dynamic Internet Technology domain dfgvx.com [**]  [Classification: Misc activity] [Priority: 3] [VRF: 10] {UDP} 192.168.60.2:48517 -> 208.67.222.222:53
 ```
 
## URL Filtering Statistics

On vManage, URL filtering statistics are shown based on categories and it can be retrieved using below sample API queries. 

## Resource URL

 
```
https://<vmanage-ip>/dataservice/statistics/urlf/aggregation
```
 

## Query to fetch blocked statistics

 
use metrics `property = block` , In order fetch blocked URL categories count.

 

```
{
  "aggregation": {
    "metrics": [
      {
        "property": "block",
        "type": "sum",
        "size": 25,
        "order": "desc"
      }
    ],
    "field": [
      {
        "property": "name",
        "sequence": 1,
        "size": 25
      }
    ]
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
          "urlf_category"
        ],
        "field": "type",
        "type": "string",
        "operator": "in"
      }
    ]
  }
}
 ```

## Sample Response

 
```
  "data": [
    {
      "name": "Gambling",
      "count": 2296,
      "block": 4315
    },
    {
      "name": "Auctions",
      "count": 2296,
      "block": 1439
    },
    {
      "name": "Religion",
      "count": 2296,
      "block": 1437
    },
    {
      "name": "Abortion",
      "count": 2296,
      "block": 0
    },
    {
      "name": "Abused Drugs",
      "count": 2296,
      "block": 0
    },

<snip>
```

## Query to fetch allowed statistics


use metrics `property = pass` , In order to fetch allowed URL categories count.

 
```
{
  "aggregation": {
    "metrics": [
      {
        "property": "pass",
        "type": "sum",
        "order": "desc",
        "size": 25
      }
    ],
    "field": [
      {
        "property": "name",
        "sequence": 1,
        "size": 25
      }
    ]
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
          "urlf_category"
        ],
        "field": "type",
        "type": "string",
        "operator": "in"
      }
    ]
  }
}
```

## Sample Response 

```
  "data": [
    {
      "name": "Computer and Internet Info",
      "count": 2304,
      "pass": 25807
    },
    {
      "name": "Social Network",
      "count": 2304,
      "pass": 15844
    },
    {
      "name": "Online Personal Storage",
      "count": 2304,
      "pass": 10086
    },
<snip>
```

## Query to fetch whitelist hit count:

```
{
  "aggregation": {
    "metrics": [
      {
        "property": "whitelist_hit_cnt",
        "type": "sum"
      }
    ]
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
          "urlf"
        ],
        "field": "type",
        "type": "string",
        "operator": "in"
      }
    ]
  }
}
```

### Sample response: 

 
```
"data": [
    {
      "whitelist_hit_cnt": 2291
    }
  ]
```
 

## Query to fetch blacklist hit count:

 
```
{
  "aggregation": {
    "metrics": [
      {
        "property": "blacklist_hit_cnt",
        "type": "sum"
      },
      {
        "property": "reputation_block",
        "type": "sum"
      }
    ]
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
          "urlf"
        ],
        "field": "type",
        "type": "string",
        "operator": "in"
      }
    ]
  }
}
```
 

### Sample Response: 

 
```
"data": [
    {
      "reputation_block": 1438,
      "blacklist_hit_cnt": 0
    }
       ]
```
 

In order to find URL's that are blocked/dropped, we can use command "show utd engine standard logging events" on XE-SDWAN CLI

 

 
```
BR2-CSR1000v#show utd engine standard logging events | i UTD
2019/05/07-04:10:49.178868 UTC [**] [Hostname: 1.1.1.6] [**] [Instance_ID: 1] [**] Drop [**] UTD WebFilter Category/Reputation [**] [URL: twitter.com] ** [Category: Social Network] ** [Reputation: 92] [VRF: 10] {TCP} 192.168.40.2:34878 -> 104.244.42.129:443
2019/05/07-04:10:50.847634 UTC [**] [Hostname: 1.1.1.6] [**] [Instance_ID: 1] [**] Drop [**] UTD WebFilter Category/Reputation [**] [URL: jw.org/] ** [Category: Religion] ** [Reputation: 96] [VRF: 10] {TCP} 23.205.63.223:80 -> 192.168.40.2:36844
2019/05/07-04:10:50.893649 UTC [**] [Hostname: 1.1.1.6] [**] [Instance_ID: 1] [**] Drop [**] UTD WebFilter Category/Reputation [**] [URL: jw.org/favicon.ico] ** [Category: Religion] ** [Reputation: 96] [VRF: 10] {TCP} 23.205.63.223:80 -> 192.168.40.2:36846
2019/05/07-04:11:00.277013 UTC [**] [Hostname: 1.1.1.6] [**] [Instance_ID: 1] [**] Drop [**] UTD WebFilter Category/Reputation [**] [URL: twitter.com] ** [Category: Social Network] ** [Reputation: 92] [VRF: 10] {TCP} 192.168.40.2:34888 -> 104.244.42.129:443
2019/05/07-04:11:01.941105 UTC [**] [Hostname: 1.1.1.6] [**] [Instance_ID: 1] [**] Drop [**] UTD WebFilter Category/Reputation [**] [URL: jw.org/] ** [Category: Religion] ** [Reputation: 96] [VRF: 10] {TCP} 23.205.63.223:80 -> 192.168.40.2:36854
2019/05/07-04:11:01.973286 UTC [**] [Hostname: 1.1.1.6] [**] [Instance_ID: 1] [**] Drop [**] UTD WebFilter Category/Reputation [**] [URL: jw.org/favicon.ico] ** [Category: Religion] ** [Reputation: 96] [VRF: 10] {TCP} 23.205.63.223:80 -> 192.168.40.2:36856
2019/05/07-04:11:11.376268 UTC [**] [Hostname: 1.1.1.6] [**] [Instance_ID: 1] [**] Drop [**] UTD WebFilter Category/Reputation [**] [URL: twitter.com] ** [Category: Social Network] ** [Reputation: 92] [VRF: 10] {TCP} 192.168.40.2:34898 -> 104.244.42.129:443
2019/05/07-04:11:13.045320 UTC [**] [Hostname: 1.1.1.6] [**] [Instance_ID: 1] [**] Drop [**] UTD WebFilter Category/Reputation [**] [URL: jw.org/] ** [Category: Religion] ** [Reputation: 96] [VRF: 10] {TCP} 23.205.63.223:80 -> 192.168.40.2:36864
```