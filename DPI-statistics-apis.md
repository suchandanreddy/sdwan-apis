# QoS Monitoring APIs

## Resource URL: 

https://vmanage-ip/dataservice/device/policy/accesslistpolicers?deviceId=system-ip

## Method: 

GET

## Sample Response: 

```
[{'name': 'QOS-ACL', 
  'lastupdated': 1562748821183, 
  'vdevice-dataKey': '1.1.1.6-QOS-ACL-', 
  'vdevice-name': '1.1.1.6', 
  'vdevice-host-name': 
  'BR-CSR1000v-2'}]
```

# Application SLA Changes

## Resource URL: 

https://vmanage-ip/dataservice/event/aggregation

## Method: 

POST

## Sample Payload

```json
{
  "query": {
    "condition": "AND",
    "rules": [
      {
        "value": [
          "3"
        ],
        "field": "entry_time",
        "type": "date",
        "operator": "last_n_hours"
      },
      {
        "value": [
          "App-Route"
        ],
        "field": "component",
        "type": "string",
        "operator": "in"
      },
      {
        "value": [
          "sla-violation-pkt-drop",
          "sla-config",
          "sla-change",
          "sla-violation"
        ],
        "field": "eventname",
        "type": "string",
        "operator": "in"
      }
    ]
  },
  "aggregation": {
    "field": [
      {
        "property": "severity_level",
        "order": "asc",
        "sequence": 1
      }
    ],
    "histogram": {
      "property": "entry_time",
      "interval": 1,
      "type": "hour",
      "order": "asc"
    }
  }
}
```

# Application Bandwidth Usage

## Resource URL: 

https://vmanage-ip/dataservice/statistics/dpi/aggregation

## Method: 

POST

## Sample Query Payload: 

```json
{"query":{"condition":"AND",
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
                                 
                                 "metrics":[{"property":"octets","type":"sum","order":"desc"}]}}
```

## Sample Response: 

```
[{'application': 'http', 'count': 572, 'octets': 409734}, 
 {'application': 'godaddy', 'count': 10, 'octets': 7258}, 
 {'application': 'amazon-web-services', 'count': 26, 'octets': 3211}, 
 {'application': 'pocket', 'count': 16, 'octets': 1460},
 {'application': 'hubspot', 'count': 8, 'octets': 932},
 {'application': 'akamai', 'count': 10, 'octets': 930}, 
 {'application': 'nytimes', 'count': 4, 'octets': 490}, 
 {'application': 'cnn', 'count': 4, 'octets': 482},
 {'application': 'washington-post', 'count': 4, 'octets': 474}, 
 {'application': 'youtube', 'count': 4, 'octets': 452},
 {'application': 'github', 'count': 4, 'octets': 324}, 
 {'application': 'twitter', 'count': 4, 'octets': 272}]
```

