# Example 1

Interface statistics Simple Query API call to fectch the interface statistics for all the interfaces in the network for 30 mins interval. 

## API URL:

`https://{{vmanage}}:{{port}}/dataservice/statistics/interface`

## Method:

POST

## Query:

```
{
  "query": {
    "condition": "AND",
    "rules": [
        {
            "value": [
                        "2020-10-20T10:00:00 UTC",
                        "2020-10-20T10:30:00 UTC" 
                     ],
            "field": "entry_time",
            "type": "date",
            "operator": "between"
        }
    ]
  }
}
```

## Sample Response

```
    "data": [
        {
            "down_capacity_percentage": 0,
            "tx_pps": 0,
            "total_mbps": 0,
            "device_model": "vedge-CSR-1000v",
            "rx_kbps": 0,
            "interface": "Tunnel100001",
            "tx_octets": 0,
            "oper_status": "Down",
            "rx_errors": 0,
            "bw_down": 100,
            "tx_pkts": 0,
            "tx_errors": 0,
            "rx_octets": 0,
            "statcycletime": 1603190400016,
            "admin_status": "Up",
            "bw_up": 100,
            "interface_type": "logical",
            "tenant": "default",
            "entry_time": 1603189563640,
            "rx_pkts": 0,
            "af_type": "IPv4",
            "rx_pps": 0,
            "vmanage_system_ip": "1.1.1.6",
            "tx_drops": 0,
            "rx_drops": 0,
            "tx_kbps": 0,
            "vdevice_name": "1.1.1.6",
            "up_capacity_percentage": 0,
            "vip_idx": 16,
            "host_name": "BR2-CSR1000v",
            "vpn_id": 0,
            "id": "Ju2YRXUB6FA-Z7p5JO8f"
        },
        {
            "down_capacity_percentage": 0,
            "tx_pps": 0,
            "total_mbps": 0,
            "device_model": "vedge-CSR-1000v",
            "rx_kbps": 0,
            "interface": "Tunnel100002",
            "tx_octets": 0,
            "oper_status": "Down",
            "rx_errors": 0,
            "bw_down": 100,
            "tx_pkts": 0,
            "tx_errors": 0,
            "rx_octets": 0,
            "statcycletime": 1603190400017,
            "admin_status": "Up",
            "bw_up": 100,
            "interface_type": "logical",
            "tenant": "default",
            "entry_time": 1603189563640,
            "rx_pkts": 0,
            "af_type": "IPv4",
            "rx_pps": 0,
            "vmanage_system_ip": "1.1.1.6",
            "tx_drops": 0,
            "rx_drops": 0,
            "tx_kbps": 0,
            "vdevice_name": "1.1.1.6",
            "up_capacity_percentage": 0,
            "vip_idx": 17,
            "host_name": "BR2-CSR1000v",
            "vpn_id": 0,
            "id": "J-2YRXUB6FA-Z7p5JO8f"
        },
```

# Example 2

Interface statistics Aggregation Query API to retrieve sum of octets for each interface in a given Service VPN of device with system-ip "1.1.2.1" for last 12 hours.

## API URL:

`https://{{vmanage}}:{{port}}/dataservice/statistics/interface/aggregation`

## Method:

POST

## Query:

<pre>
{
  "query": {
    "condition": "AND",
    "rules": [
      {
        "value": [
          <b>"12"</b>
        ],
        "field": "entry_time",
        "type": "date",
        <b>"operator": "last_n_hours"</b>
      },
      {
        "value": [
          <b>"1.1.2.1"</b>
        ],
        <b>"field": "vdevice_name",</b>
        "type": "string",
        "operator": "in"
      },
      {
        "value": [
          <b>"1"</b>
        ],
        <b>"field": "vpn_id",</b>
        "type": "number",
        "operator": "in"
      }
    ]
  },
  "aggregation": {
    "field": [
      {
        "property": "interface",
        "sequence": 1
      }
    ],
    "metrics": [
      {
        <b>"property": "rx_octets",
        "type": "sum"</b>
      },
      {
        <b>"property": "tx_octets",
        "type": "sum"</b>
      }
    ]
  }
}
</pre>

## Sample Response:

```
    "data": [
        {
            "interface": "ge0/2",
            "count": 70,
            "rx_octets": 32509568,
            "tx_octets": 260399334
        },
        {
            "interface": "loopback1",
            "count": 70,
            "rx_octets": 0,
            "tx_octets": 0
        }
    ]
```

# Example 3

Interface statistics Aggregation Query API to retrieve sum of octets for each interface in a given Service VPN across all devices in the fabric for last 12 hours

## Query:

<pre>
{
  "query": {
    "condition": "AND",
    "rules": [
      {
        "value": [
          <b>"12"</b>
        ],
        "field": "entry_time",
        "type": "date",
        <b>"operator": "last_n_hours"</b>
      },
      {
        "value": [
          <b>"1"</b>
        ],
        <b>"field": "vpn_id",</b>
        "type": "number",
        "operator": "in"
      }
    ]
  },
  "aggregation": {
    "field": [
      {
        "property": "interface",
        "sequence": 1
      },
      {
        "property": "vdevice_name",
        "sequence": 2
      },
      {
        "property": "vpn_id",
        "sequence": 3
      }
    ],
    "metrics": [
      {
        <b>"property": "rx_octets",
        "type": "sum"</b>
      },
      {
        <b>"property": "tx_octets",
        "type": "sum"</b>
      }
    ]
  }
}
</pre>

## Sample Response

```
    "data": [
        {
            "interface": "ge0/2",
            "count": 72,
            "vdevice_name": "1.1.2.211",
            "vpn_id": "1",
            "rx_octets": 261953,
            "tx_octets": 156828
        },
        {
            "interface": "ge0/2",
            "count": 72,
            "vdevice_name": "1.1.2.5",
            "vpn_id": "1",
            "rx_octets": 241920,
            "tx_octets": 0
        },
        {
            "interface": "ge0/2",
            "count": 71,
            "vdevice_name": "1.1.2.210",
            "vpn_id": "1",
            "rx_octets": 257941,
            "tx_octets": 154526
        },
        {
            "interface": "ge0/2",
            "count": 70,
            "vdevice_name": "1.1.2.1",
            "vpn_id": "1",
            "rx_octets": 32509568,
            "tx_octets": 260399334
        },
        {
            "interface": "ge0/2",
            "count": 70,
            "vdevice_name": "1.1.2.200",
            "vpn_id": "1",
            "rx_octets": 266279454,
            "tx_octets": 20932398
        },
<snip>
```