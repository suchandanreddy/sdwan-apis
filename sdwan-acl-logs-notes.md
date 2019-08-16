# vManage APIs for ACL logs

## Resource URL:

-	https://vmanage-ip/dataservice/statistics/flowlog

## Method: 

-	POST

## Constructing Query: 

-	By using GET request on the URL `https://vmanage-ip/dataservice/statistics/flowlog/fields` we can retrieve the list of fields that can be
    used while constructing the query. 

**Sample Response:**

-	Here is the sample response for Query fields that are supported for ACL logs. 

```
[
    {
        "dataType": "string",
        "property": "vdevice_name"
    },
    {
        "dataType": "string",
        "property": "host_name"
    },
    {
        "dataType": "date",
        "property": "entry_time"
    },
    {
        "dataType": "number",
        "property": "vpn_id"
    },
    {
        "dataType": "string",
        "property": "src_ip"
    },
    {
        "dataType": "string",
        "property": "dest_ip"
    },
    {
        "dataType": "string",
        "property": "src_port"
    },
    {
        "dataType": "number",
        "property": "dest_port"
    },
    {
        "dataType": "number",
        "property": "dscp"
    },
    {
        "dataType": "number",
        "property": "ip_proto"
    },
    {
        "dataType": "string",
        "property": "action"
    },
    {
        "dataType": "string",
        "property": "direction"
    },
    {
        "dataType": "date",
        "property": "statcycletime"
    },
    {
        "dataType": "number",
        "property": "vip_idx"
    },
    {
        "dataType": "date",
        "property": "vip_time"
    },
    {
        "dataType": "string",
        "property": "ingress_intf"
    },
    {
        "dataType": "string",
        "property": "egress_intf"
    },
    {
        "dataType": "string",
        "property": "policy_name"
    },
    {
        "dataType": "date",
        "property": "start_time"
    },
    {
        "dataType": "number",
        "property": "total_pkts"
    },
    {
        "dataType": "number",
        "property": "total_bytes"
    },
    {
        "dataType": "number",
        "property": "flow_active"
    },
    {
        "dataType": "string",
        "property": "device_model"
    }
]
```

**Sample Query:**

Using above supported fields a query can be built to retrieve the relevant logs. 

Here is the query to retrieve the last 24 hours ACL logs for policy `_vpn1_data` and the egress interface is `ge0/5`

```
{ "query" : {"condition": "AND", 
                      "rules":
                      [{"value":["24"],"field":"entry_time","type":"date","operator":"last_n_hours"},
                       {"value":["_vpn1_data"],"field":"policy_name","type":"string","operator":"in"},
                       {"value":["ge0/5"],"field":"egress_intf","type":"string","operator":"in"}]}}
```

**Sample Response** 

Below are the various fields viz. action, source and destination ip address, device-id for each ACL log that is received from vManage. 

```
$python3 sdwan-acl-logs.py

[
    {
        "action": "accept",
        "dest_ip": "192.168.10.9",
        "dest_port": 68,
        "device_model": "vedge-cloud",
        "direction": "from-service",
        "dscp": 0,
        "egress_intf": "ge0/5",
        "entry_time": 1565903850797,
        "flow_active": "TRUE",
        "host_name": "vEdge-1",
        "id": "AWyXOSQH5I6sVUD3_95w",
        "ingress_intf": "cpu",
        "ip_proto": 17,
        "policy_name": "_vpn1_data",
        "src_ip": "192.168.10.1",
        "src_port": 67,
        "start_time": 1565903850000,
        "statcycletime": 1565905200133,
        "tenant": "default",
        "total_bytes": 342,
        "total_pkts": 1,
        "vdevice_name": "1.1.1.7",
        "vmanage_system_ip": "1.1.1.7",
        "vpn_id": 1
    }
]
```