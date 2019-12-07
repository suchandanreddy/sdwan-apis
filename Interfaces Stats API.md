# Example 1

Interface statistics query to retrieve sum of octets for each interface in a given Service VPN of device with system-ip "1.1.2.1" for last 12 hours.

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

# Example 2

Interface statistics query to retrieve sum of octets for each interface in a given Service VPN across all devices in the fabric for last 12 hours

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