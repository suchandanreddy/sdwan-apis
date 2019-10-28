This article covers the API responses formats for various features in SD-WAN Security.

Table of Contents
=================

   * [UTD Container status](#utd-container-status)

   * [Enterprise Zone based Firewall](#enterprise-zone-based-firewall)

   * [IPS Alerts](#ips-alerts)

   * [URL Filtering Statistics](#url-filtering-statistics)
      * [Query to fetch blocked statistics](#query-to-fetch-blocked-statistics)
      * [Query to fetch allowed statistics](#query-to-fetch-allowed-statistics)
      * [Query to fetch whitelist hit count:](#query-to-fetch-whitelist-hit-count)
      * [Query to fetch blacklist hit count:](#query-to-fetch-blacklist-hit-count)

   * [Umbrella](#umbrella)
      * [Reachability to Umbrella Cloud](#reachability-to-umbrella-cloud)
      * [Number of DNS queries redirected](#number-of-dns-queries-redirected)

   * [AMP / TG](#amp--tg)
      * [Reachability to AMP / TG cloud](#reachability-to-amp--tg-cloud)
      * [File reputation status](#file-reputation-status)
      * [File analysis status](#file-analysis-status)
      * [Number of files analyzed by AMP](#number-of-files-analyzed-by-amp)
      * [Numbers of files sent to TG](#numbers-of-files-sent-to-tg)
      * [Disposition of Files Scanned](#disposition-of-files-scanned)
      * [Retrospective Alerts](#retrospective-alerts)


# UTD Container status

**URL:** `https://<vmanage-ip>/dataservice/device/utd/engine-instance-status?deviceId=<device-id/system-ip>`

## Response

```
    {
      "utd-engine-instance-status-running": "true",
      "vdevice-dataKey": "1.1.1.6-1",
      "vdevice-name": "1.1.1.6",
      "utd-engine-instance-status-id": "1",
      "utd-engine-instance-status-status": "utd-oper-status-green",
      "lastupdated": 1572238580952,
      "vdevice-host-name": "BR-CSR1000v-2"
    }
```

**URL:** `https://<vmanage-ip>/dataservice/device/utd/ips-update-status?deviceId=<device-id/system-ip>`

## Response

```
    {
      "ips-update-status-last-update-time": "1970-01-01T00:00:00+00:00",
      "ips-update-status-version": "29.0.c",
      "vdevice-dataKey": "1.1.1.6",
      "vdevice-name": "1.1.1.6",
      "lastupdated": 1572238663422,
      "ips-update-status-last-update-status": "utd-update-status-unknown",
      "vdevice-host-name": "BR-CSR1000v-2",
      "ips-update-status-last-successful-update-time": "1970-01-01T00:00:00+00:00"
    }
```

**URL:** `https://<vmanage-ip>/dataservice/device/utd/engine-status?deviceId=<device-id/system-ip>`

## Response

```
    {
      "vdevice-dataKey": "1.1.1.6",
      "utd-engine-status-version": "1.0.8_SV2.9.11.1_XE16.10",
      "vdevice-name": "1.1.1.6",
      "utd-engine-status-memory-status": "utd-oper-status-green",
      "lastupdated": 1572238734476,
      "utd-engine-status-status": "utd-oper-status-green",
      "utd-engine-status-memory-usage": "13.2",
      "vdevice-host-name": "BR-CSR1000v-2",
      "utd-engine-status-profile": "Cloud-Low"
    }
```

# Enterprise Zone based Firewall

**URL:** `https://{{vmanage}}:{{port}}/dataservice/statistics/fwall/aggregation`

# Sample Query: 

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
          "proto"
        ],
        "field": "type",
        "type": "string",
        "operator": "in"
      }
    ]
  },
  "aggregation": {
    "metrics": [
      {
      	"property":"byte_counters",
    	"type":"sum"
      },
      { 
      	"property":"app_name",
      	"type":"cardinality"
      }
    ],
    "field": [
      {
        "property": "class_name"
      },
      {
      "property": "vdevice_name"
      }
    ]
  }
}
```


## Sample Response

```
        {
            "class_name": "class-default",
            "count": 31293,
            "vdevice_name": "1.1.1.5",
            "app_name": 0,
            "byte_counters": 116411
        },
        {
            "class_name": "class-default",
            "count": 29505,
            "vdevice_name": "1.1.1.6",
            "app_name": 0,
            "byte_counters": 119311
        },
        {
            "class_name": "BR1-FW-VPN10-seq-1-cm_",
            "count": 31293,
            "vdevice_name": "1.1.1.5",
            "app_name": 0,
            "byte_counters": 59087980671927
        },
        {
            "class_name": "BRANCH-DIA-VPN10-seq-1-cm_",
            "count": 29505,
            "vdevice_name": "1.1.1.6",
            "app_name": 0,
            "byte_counters": 38459474478632
        }
```

# IPS Alerts

**URL:** `https://{{vmanage}}:{{port}}/dataservice/statistics/ipsalert/aggregation`

## Sample Query

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
          "ips_alert"
        ],
        "field": "type",
        "type": "string",
        "operator": "in"
      }
    ]
  },
  "aggregation": {
    "field": [
      {
        "property": "entry_time",
        "dataType": "date"
      },
      {
        "property": "device_model",
        "dataType": "string"
      },
      {
        "property": "vdevice_name",
        "dataType": "string"
      },
      {
        "property": "host_name",
        "dataType": "string"
      },
      {
        "property": "vrf",
        "dataType": "number"
      },
      {
        "property": "message",
        "dataType": "string"
      },
      {
        "property": "src_ip",
        "dataType": "string"
      },
      {
        "property": "src_port",
        "dataType": "number"
      },
      {
        "property": "dst_ip",
        "dataType": "string"
      },
      {
        "property": "dst_port",
        "dataType": "number"
      },
      {
        "property": "protocol",
        "dataType": "number"
      },
      {
        "property": "action",
        "dataType": "number"
      },
      {
        "property": "sid",
        "dataType": "number"
      },
      {
        "property": "gid",
        "dataType": "number"
      },
      {
        "property": "violation_path",
        "dataType": "string"
      },
      {
        "property": "type",
        "dataType": "string"
      }
    ]
  }
}
```


## Sample Response

```
{
    "entry_time": "2019-10-28T03:40:00.004Z",
    "count": 4,
    "device_model": "vedge-CSR-1000v",
    "vdevice_name": "1.1.1.5",
    "host_name": "BR1-CSR1000v",
    "vrf": "10",
    "message": "MALWARE-OTHER DNS request for known malware domain toknowall.com - Unix.Trojan.Vpnfilter",
    "src_ip": "192.168.60.2",
    "src_port": "44040",
    "dst_ip": "8.8.8.8",
    "dst_port": "53",
    "protocol": "17",
    "action": "2",
    "sid": "46807",
    "gid": "1",
    "violation_path": "192.168.60.2:8.8.8.8",
    "type": "ips_alert"
}
```

Note: Above dictonary response is available for each IPS alert

## URL Filtering Statistics

On vManage, URL filtering statistics are shown based on categories and it can be retrieved using below sample API queries. 

## Resource URL

**URL:** `https://<vmanage-ip>/dataservice/statistics/urlf/aggregation`

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

# Umbrella

## Reachability to Umbrella Cloud

**URL:** `https://<vmanage-ip>/dataservice/device/umbrella/device-registration?deviceId=<device-id/system-ip>`

```
{
  "vdevice-dataKey": "1.1.1.6-10",
  "vdevice-name": "1.1.1.6",
  "umbrella-dev-reg-data-tag": "vpn10",
  "umbrella-dev-reg-data-name": "10",
  "lastupdated": 1572246207456,
  "umbrella-dev-reg-data-device-id": "010ad45ad4edba4a",
  "vdevice-host-name": "BR-CSR1000v-2",
  "umbrella-dev-reg-data-status": "200 SUCCESS"
}
```

## Number of DNS queries redirected

**URL:** `https://<vmanage-ip>/dataservice/statistics/umbrella/aggregation`

```
{
  "query": {
    "condition": "AND",
    "rules": [
      {
        "value": [
          "10"
        ],
        "field": "entry_time",
        "type": "date",
        "operator": "last_n_hours"
      },
      {
        "value": [
          "umbrella"
        ],
        "field": "type",
        "type": "string",
        "operator": "in"
      }
    ]
  },
  "aggregation": {
    "metrics": [
      {
        "property": "redirect_pkts",
        "type":"sum"
      }
    ],
    "field" : [
     {
      	"property":"vdevice_name",
      	"dataType": "string"
     }
    ],
    "histogram": {
      "property": "entry_time",
      "type": "minute",
      "interval": 60,
      "order": "asc"
    }
  }
}
```

## Sample Response: 

```
{
    "entry_time": 1572217200000,
    "count": 10,
    "vdevice_name": "1.1.1.5",
    "redirect_pkts": 0
},
{
    "entry_time": 1572217200000,
    "count": 8,
    "vdevice_name": "1.1.1.6",
    "redirect_pkts": 2641
}
```

# AMP / TG

## Reachability to AMP / TG cloud

## File reputation status

**URL:** `https://<vmanage-ip>/dataservice/device/utd/file-reputation-status?deviceId=<device-id/system-ip>`

### Sample Response

```
    {
      "vdevice-dataKey": "1.1.2.3",
      "utd-file-reputation-status-status": "utd-file-repu-stat-connected",
      "vdevice-name": "1.1.2.3",
      "lastupdated": 1572250935199,
      "utd-file-reputation-status-message": "Connected to AMP Cloud!",
      "utd-file-reputation-status-version": "1.12.4.999",
      "vdevice-host-name": "RemoteSite3-4K"
    }
```

## File analysis status

**URL:** `https://<vmanage-ip>/dataservice/device/utd/file-analysis-status?deviceId=<device-id/system-ip>`

### Sample Response

```
 {
   "utd-file-analysis-status-message": "TG Process Up",
   "utd-file-analysis-status-status": "tg-client-stat-up",
   "vdevice-dataKey": "1.1.2.3",
   "vdevice-name": "1.1.2.3",
   "lastupdated": 1572250947074,
   "utd-file-analysis-status-backoff-interval": "0",
   "vdevice-host-name": "RemoteSite3-4K"
 }
```

## Number of files analyzed by AMP

**URL:** `https://<vmanage-ip>/dataservice/statistics/urlf/aggregation`

### Sample Query

```
{
  "query": {
    "condition": "AND",
    "rules": [
      {
        "value": [
          "12"
        ],
        "field": "entry_time",
        "type": "date",
        "operator": "last_n_hours"
      },
      {
        "value": [
          "amp"
        ],
        "field": "type",
        "type": "string",
        "operator": "in"
      }
    ]
  },
  "aggregation": {
    "metrics": [
      {
        "property": "amp_file_malicious_cnt",
        "type": "sum"
      },
      {
        "property": "amp_file_unknown_cnt",
        "type": "sum"
      },
      {
        "property": "amp_file_clean_cnt",
        "type": "sum"
      }
    ],
	"field" : [
     {
      	"property":"vdevice_name",
      	"dataType": "string"
     }
     ]
  }
}
```

### Sample Response

```
 {
    "vdevice_name": "1.1.2.3",
    "count": 1144,
    "amp_file_malicious_cnt": 8,
    "amp_file_clean_cnt": 0,
    "amp_file_unknown_cnt": 0
 }
```

## Numbers of files sent to TG

**URL:** `https://<vmanage-ip>/dataservice/statistics/urlf`

### Sample Query

```
{
  "query": {
    "condition": "AND",
    "rules": [
      {
        "value": [
          "12"
        ],
        "field": "entry_time",
        "type": "date",
        "operator": "last_n_hours"
      },
      {
        "value": [
          "file_analysis_notif"
        ],
        "field": "type",
        "type": "string",
        "operator": "in"
      }
    ]
  }
}
```

## Disposition of Files Scanned

**URL:** `https://<vmanage-ip>/dataservice/statistics/urlf`

### Sample Query 

```
{
  "query": {
    "condition": "AND",
    "rules": [
      {
        "value": [
          "12"
        ],
        "field": "entry_time",
        "type": "date",
        "operator": "last_n_hours"
      },
      {
        "value": [
          "file_reputation_alert"
        ],
        "field": "type",
        "type": "string",
        "operator": "in"
      }
    ]
  }
}
```

### Sample Response

```
   {
      "entry_time": 1572250770000,
      "filetype": "EICAR",
      "device_model": "vedge-ISR-4331",
      "actionValue": "Drop",
      "vrf": 1,
      "vmanage_system_ip": "1.1.2.3",
      "type": "file_reputation_alert",
      "dst_ip": "192.168.150.2",
      "src_ip": "213.211.198.62",
      "src_port": 20480,
      "disposition": 1,
      "protocol": 6,
      "filename": "download/eicar.com.txt",
      "vdevice_name": "1.1.2.3",
      "statcycletime": 1572249600813,
      "dst_port": 50337,
      "action": 2,
      "dispositionValue": "Malicious",
      "filehash": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
      "host_name": "RemoteSite3-4K",
      "tenant": "default",
      "id": "AW4RYQM6t-0G_xeQh0mz"
    },
    {
      "entry_time": 1572250768000,
      "filetype": "EICAR",
      "device_model": "vedge-ISR-4331",
      "actionValue": "Drop",
      "vrf": 1,
      "vmanage_system_ip": "1.1.2.3",
      "type": "file_reputation_alert",
      "dst_ip": "192.168.150.2",
      "src_ip": "213.211.198.62",
      "src_port": 20480,
      "disposition": 1,
      "protocol": 6,
      "filename": "download/eicar.com.txt",
      "vdevice_name": "1.1.2.3",
      "statcycletime": 1572249600813,
      "dst_port": 49825,
      "action": 2,
      "dispositionValue": "Malicious",
      "filehash": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
      "host_name": "RemoteSite3-4K",
      "tenant": "default",
      "id": "AW4RYQM6t-0G_xeQh0my"
    },
    <snip>
```

**Note:**  Above dictonary response is available for each file that is analysed by AMP. 

## Retrospective Alerts

**URL:** `https://<vmanage-ip>/dataservice/statistics/urlf`

### Sample Query

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
          "file_retrospective_alert"
        ],
        "field": "type",
        "type": "string",
        "operator": "in"
      }
    ]
  }
}
```