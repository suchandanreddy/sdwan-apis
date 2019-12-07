# Example 1

Interface statistics query to retrieve sum of octets for each interface in a given Service VPN of device with system-ip "1.1.2.1"

## API URL:

`https://{{vmanage}}:{{port}}/dataservice/statistics/interface/aggregation`

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
          "12"
        ],
        "field": "entry_time",
        "type": "date",
        "operator": "last_n_hours"
      },
      {
        "value": [
          "1.1.2.1"
        ],
        "field": "vdevice_name",
        "type": "string",
        "operator": "in"
      },
      {
        "value": [
          "1"
        ],
        "field": "vpn_id",
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
        "property": "rx_octets",
        "type": "sum"
      },
      {
        "property": "tx_octets",
        "type": "sum"
      }
    ]
  }
}
```

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

# Example 2

Interface statistics query to retrieve sum of octets for each interface in a given Service VPN across all devices in the fabric.

## Query:

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
          "1"
        ],
        "field": "vpn_id",
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
        "property": "rx_octets",
        "type": "sum"
      },
      {
        "property": "tx_octets",
        "type": "sum"
      }
    ]
  }
}
```

## Sample Response

```
    "data": [
        {
            "interface": "loopback1",
            "count": 72,
            "vdevice_name": "1.1.1.10",
            "vpn_id": "1",
            "rx_octets": 0,
            "tx_octets": 0
        },
        {
            "interface": "loopback1",
            "count": 72,
            "vdevice_name": "1.1.2.211",
            "vpn_id": "1",
            "rx_octets": 0,
            "tx_octets": 0
        },
        {
            "interface": "loopback1",
            "count": 72,
            "vdevice_name": "1.1.2.4",
            "vpn_id": "1",
            "rx_octets": 0,
            "tx_octets": 0
        },
        {
            "interface": "loopback1",
            "count": 72,
            "vdevice_name": "1.1.2.5",
            "vpn_id": "1",
            "rx_octets": 0,
            "tx_octets": 0
        },
        {
            "interface": "loopback1",
            "count": 72,
            "vdevice_name": "31.31.31.2",
            "vpn_id": "1",
            "rx_octets": 0,
            "tx_octets": 0
        },
        {
            "interface": "loopback1",
            "count": 71,
            "vdevice_name": "1.1.1.11",
            "vpn_id": "1",
            "rx_octets": 0,
            "tx_octets": 0
        },
<snip>
```