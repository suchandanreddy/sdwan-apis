
**Application Aware Routing Statistics (Latency/Loss/Jitter) Query APIs**

**API Endpoint:**

https://{{vmanage}}:{{port}}/dataservice/statistics/approute/page?scrollId=&count=5000

**Method:**

POST

**Query Payload:**

```
{
  "query": {
    "condition": "AND",
    "rules": [
      {
        "value": [              
          "2020-06-01T03:00:00 UTC",
          "2020-06-01T03:05:00 UTC"
        ],
        "field": "entry_time",
        "type": "date",
        "operator": "between"
      }
    ]
  },
  "fields":
  [
    "latency",
    "jitter",
    "entry_time",
    "name",
    "local_system_ip",
    "remote_system_ip",
    "local_color",
    "remote_color",
    "src_ip",
    "dst_ip",
    "loss_percentage"
  ]
}
```

**API Endpoint:**

https://{{vmanage}}:{{port}}/dataservice/statistics/dpi/page?count=200

**Method:**

POST

**Query Payload:**

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
          "mpls"
        ],
        "field": "local_color",
        "type":"string",
        "operator":"in"
      }
    ]
  }
}
```
**BFD Sessions**

**API Endpoint:**

https://{{vmanage}}:{{port}}/dataservice/device

**Method:**

GET

**Sample Response**

For each device in the inventory we have below dictonary in this API response. We can use the `bfdSessionsUp` value and add to get the total number of BFD sessions in the overlay. 

```
      {
            "deviceId": "1.1.1.110",
            "system-ip": "1.1.1.110",
            "host-name": "AWS-vEdge-1",
            "reachability": "reachable",
            "status": "normal",
            "personality": "vedge",
            "device-type": "vedge",
            "timezone": "UTC",
            "device-groups": [
            ],
            "lastupdated": 1588328761611,
            "bfdSessionsUp": 3,
            "domain-id": "1",
            "board-serial": "3C",
            "certificate-validity": "Valid",
            "max-controllers": "0",
            "uuid": "811c79c3-ca03-44cd-a66a-804a06f7edf0",
            "bfdSessions": "3",
            "controlConnections": "2",
            "device-model": "vedge-cloud",
            "version": "18.3.0",
            "connectedVManages": [
                "\"1.1.1.2\""
            ],
            "site-id": "1000",
            "ompPeers": "1",
            "latitude": "37.666684",
            "longitude": "-122.777023",
            "isDeviceGeoData": false,
            "platform": "x86_64",
            "uptime-date": 1587746040000,
            "statusOrder": 4,
            "device-os": "next",
            "validity": "valid",
            "state": "green",
            "state_description": "All daemons up",
            "model_sku": "None",
            "local-system-ip": "1.1.1.110",
            "total_cpu_count": "4",
            "linux_cpu_count": "1",
            "testbed_mode": false,
            "layoutLevel": 4
        }
```

**Cloud onRamp for SaaS Statistics**

**API Endpoint:**

https://{{vmanage}}:{{port}}/dataservice/template/cloudx/status?appName={app-name}

**Method:**

GET