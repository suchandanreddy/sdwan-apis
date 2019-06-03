Table of Contents
=================

   * [Device Template APIs](#device-template-apis)
      * [Creating CLI Template](#creating-cli-template)
      * [Retrieve Templates list](#retrieve-templates-list)
      * [Attach Device Template](#attach-device-template)
      * [Preview Intent Configuration](#preview-intent-configuration)
      * [Attach CLI Template](#attach-cli-template)
      * [Track Template Push Status](#track-template-push-status)
      * [Create Device Template](#create-device-template)
      * [Create VPN Interface Feature Template](#create-vpn-interface-feature-template)
      * [Create VPN Feature Template](#create-vpn-feature-template)
      * [Create VPN 0 Interface](#create-vpn-0-interface)
      * [Attach Device Template](#attach-device-template-1)

# Device Template APIs

## Creating CLI Template

**URL:**  https://vmanage-ip:port/dataservice/template/device/cli/

**Method:** POST

**POST Request Parameters:**

```json
{
  "templateName": "",
  "templateDescription": "",
  "deviceType": "",
  "templateConfiguration": "",
  "factoryDefault": false,
  "configType": "file"
}
```

**Sample JSON Payload**

```json
{
  "templateName": "br2_vedge1",
  "templateDescription": "br2_vedge1",
  "deviceType": "vedge-cloud",
  "templateConfiguration": "system\r\n host-name               vedge\r\n admin-tech-on-failure\r\n no route-consistency-check\r\n vbond ztp.viptela.com\r\n aaa\r\n  auth-order local radius tacacs\r\n  usergroup basic\r\n   task system read write\r\n   task interface read write\r\n  !\r\n  usergroup netadmin\r\n  !\r\n  usergroup operator\r\n   task system read\r\n   task interface read\r\n   task policy read\r\n   task routing read\r\n   task security read\r\n  !\r\n  user admin\r\n   password <password-value>\r\n  !\r\n !\r\n logging\r\n  disk\r\n   enable\r\n  !\r\n !\r\n!\r\nomp\r\n no shutdown\r\n graceful-restart\r\n advertise connected\r\n advertise static\r\n!\r\nsecurity\r\n ipsec\r\n  authentication-type ah-sha1-hmac sha1-hmac\r\n !\r\n!\r\nvpn 0\r\n interface ge0/0\r\n  ip dhcp-client\r\n  ipv6 dhcp-client\r\n  tunnel-interface\r\n   encapsulation ipsec\r\n   no allow-service bgp\r\n   allow-service dhcp\r\n   allow-service dns\r\n   allow-service icmp\r\n   no allow-service sshd\r\n   no allow-service netconf\r\n   no allow-service ntp\r\n   no allow-service ospf\r\n   no allow-service stun\r\n   allow-service https\r\n  !\r\n  no shutdown\r\n !\r\n!\r\nvpn 512\r\n interface eth0\r\n  ip address <ip-address/subnet-mask>\r\n  no shutdown\r\n !\r\n ip route 0.0.0.0/0 <ip-address>\r\n!\r\n",
  "factoryDefault": false,
  "configType": "file"
}
```

**Sample Response**

{"templateId":"226c0a70-de7b-4a61-9d7e-d3da81c6102e"}

## Retrieve Templates list

**URL:** https://vmanage-ip:port/dataservice/template/device

**Method:** GET

**Sample Response:**

```json
  "data": [
    {
      "deviceType": "vedge-cloud",
      "lastUpdatedBy": "admin",
      "factoryDefault": false,
      "templateName": "br2_vedge1",
      "devicesAttached": 0,
      "templateDescription": "br2_vedge1",
      "lastUpdatedOn": 1554218933686,
      "configType": "file",
      "templateId": "226c0a70-de7b-4a61-9d7e-d3da81c6102e",
      "templateAttached": 0
    },
    {
      "deviceType": "vedge-cloud",
      "lastUpdatedBy": "admin",
      "factoryDefault": false,
      "templateName": "BR1-VE1-Template",
      "devicesAttached": 0,
      "templateDescription": "Branch1 vEdge1 Template",
      "lastUpdatedOn": 1547241442985,
      "configType": "file",
      "templateId": "21fbda48-1a53-450c-b729-be7a49c6d969",
      "templateAttached": 0
    },
    {
      "deviceType": "vsmart",
      "lastUpdatedBy": "admin",
      "factoryDefault": false,
      "templateName": "vSmartConfigurationTemplate",
      "devicesAttached": 0,
      "templateDescription": "Config template for vSmarts",
      "lastUpdatedOn": 1529606745011,
      "configType": "file",
      "templateId": "e1f3de23-1ded-49d8-85b1-1e6ab668775f",
      "templateAttached": 0
    },
    {
      "deviceType": "vedge-CSR-1000v",
      "lastUpdatedBy": "admin",
      "factoryDefault": false,
      "templateName": "BranchType1Template-CSR",
      "devicesAttached": 2,
      "templateDescription": "Branch Type 1 Template for CSR Routers",
      "lastUpdatedOn": 1550407999210,
      "configType": "template",
      "templateId": "c62e6fba-fb53-4562-b436-3878de0fbbc2",
      "templateAttached": 21
    },
    {
      "deviceType": "vedge-CSR-1000v",
      "lastUpdatedBy": "admin",
      "factoryDefault": false,
      "templateName": "BranchType3Template-CSR",
      "devicesAttached": 1,
      "templateDescription": "Branch Type 3 Template for CSR Routers",
      "lastUpdatedOn": 1548349540970,
      "configType": "template",
      "templateId": "969340a0-0e2f-4dc2-81e8-bd4534ad7aa1",
      "templateAttached": 21
    },
    {
      "deviceType": "vsmart",
      "lastUpdatedBy": "admin",
      "factoryDefault": false,
      "templateName": "VSMART-device-template",
      "devicesAttached": 2,
      "templateDescription": "vSmart device template",
      "lastUpdatedOn": 1537215263361,
      "configType": "template",
      "templateId": "55eb96ec-237d-4170-8841-3321a04e01a7",
      "templateAttached": 8
    },
    {
      "deviceType": "vedge-cloud",
      "lastUpdatedBy": "admin",
      "factoryDefault": false,
      "templateName": "BranchType2Template-vEdge",
      "devicesAttached": 0,
      "templateDescription": "Branch Type 2 Device Template",
      "lastUpdatedOn": 1551206820080,
      "configType": "template",
      "templateId": "2463357c-4261-48fe-a13e-bab7aec5c002",
      "templateAttached": 21
    },
    {
      "deviceType": "vedge-cloud",
      "lastUpdatedBy": "admin",
      "factoryDefault": false,
      "templateName": "DC-vEdges",
      "devicesAttached": 4,
      "templateDescription": "DCs with FW Service",
      "lastUpdatedOn": 1551399204233,
      "configType": "template",
      "templateId": "6c7d22bc-73d5-4877-9402-26c75a22bd08",
      "templateAttached": 19
    }
  ]
```

## Attach Device Template

**URL:** https://vmanage-ip:port/dataservice/template/device/config/input/

**Method:** POST

**POST Request Parameters:** 

{"templateId":"226c0a70-de7b-4a61-9d7e-d3da81c6102e","deviceIds":["52c7911f-c5b0-45df-b826-3155809a2a1a"],"isEdited":false,"isMasterEdited":false}
 
**Sample Response:** 

"data": [
    {
      "csv-status": "complete",
      "csv-deviceId": "52c7911f-c5b0-45df-b826-3155809a2a1a",
      "csv-deviceIP": "-",
      "csv-host-name": "-"
    }
  ]

## Preview Intent Configuration

**URL:** https://vmanage-ip:port/dataservice/template/device/config/config/

**Method:** POST

**POST Request Parameters:**

```json
{
  "templateId": "226c0a70-de7b-4a61-9d7e-d3da81c6102e",
  "device": {
    "csv-status": "complete",
    "csv-deviceId": "52c7911f-c5b0-45df-b826-3155809a2a1a",
    "csv-deviceIP": "-",
    "csv-host-name": "-",
    "csv-templateId": "226c0a70-de7b-4a61-9d7e-d3da81c6102e"
  },
  "isRFSRequired": true,
  "isEdited": false,
  "isMasterEdited": false
}
```

**Sample Response**

```viptela-system:system
   device-model            vedge-cloud
   host-name               vedge
   admin-tech-on-failure
   no route-consistency-check
   sp-organization-name    "Cisco Sy1 - 19968"
   organization-name       "Cisco Sy1 - 19968"
   vbond ztp.viptela.com port 12346
   aaa
    auth-order local radius tacacs
    usergroup basic
     task system read write
     task interface read write
    !
    usergroup netadmin
    !
    usergroup operator
     task system read
     task interface read
     task policy read
     task routing read
     task security read
    !
    user admin
     password $6$qyvManp6gTrYuozB$3hX3/03iJ36yf6.Vazv47P235HNkIQulSS.irIKpS7zfJx8Fp7NDOYfjmzvGrANGl0wBAP8el3UxNbGvzR/291
    !
   !
   logging
    disk
     enable
    !
   !
  !
  omp
   no shutdown
   graceful-restart
   advertise connected
   advertise static
  !
  security
   ipsec
    authentication-type ah-sha1-hmac sha1-hmac
   !
  !
  vpn 0
   interface ge0/0
    ip dhcp-client
    ipv6 dhcp-client
    tunnel-interface
     encapsulation ipsec
     no allow-service bgp
     allow-service dhcp
     allow-service dns
     allow-service icmp
     no allow-service sshd
     no allow-service netconf
     no allow-service ntp
     no allow-service ospf
     no allow-service stun
     allow-service https
    !
    no shutdown
   !
  !
  vpn 512
   interface eth0
    ip address <ip-address/subnet-mask>
    no shutdown
   !
   ip route 0.0.0.0/0 <ip-address>
  !
 !
!
```

## Attach CLI Template

**URL:** https://vmanage-ip:port/dataservice/template/device/config/attachcli

**Method:** POST

**POST Request Parameters:**

```json
{
  "deviceTemplateList": [
    {
      "templateId": "226c0a70-de7b-4a61-9d7e-d3da81c6102e",
      "device": [
        {
          "csv-status": "complete",
          "csv-deviceId": "52c7911f-c5b0-45df-b826-3155809a2a1a",
          "csv-deviceIP": "-",
          "csv-host-name": "-",
          "csv-templateId": "226c0a70-de7b-4a61-9d7e-d3da81c6102e"
        }
      ],
      "isEdited": false
    }
  ]
}
```

**Sample Response:** 

```json
{"id":"push_file_template_configuration-70acb6c7-a589-4a10-be93-27620c46dae5"}
```

## Track Template Push Status

**URL:** https://vmanage-ip:port/dataservice/device/action/status/push-template-id

**Method:** GET

**Sample Response:**

```json
  "data": [
    {
      "statusType": "push_file_template_configuration",
      "activity": [
        "[2-Apr-2019 15:33:06 UTC] Configuring device with cli template: br2_vedge1",
        "[2-Apr-2019 15:33:06 UTC] Generating configuration from template",
        "[2-Apr-2019 15:33:06 UTC] Checking and creating device in vManage",
        "[2-Apr-2019 15:33:07 UTC] Device is offline",
        "[2-Apr-2019 15:33:07 UTC] Updating device configuration in vManage",
        "[2-Apr-2019 15:33:08 UTC] Configuration template br2_vedge1 scheduled to be attached when device comes online. To check the synced state, click Configuration > Devices > Device Options"
      ],
      "vmanageIP": "10.10.10.10",
      "system-ip": "52c7911f-c5b0-45df-b826-3155809a2a1a",
      "deviceID": "52c7911f-c5b0-45df-b826-3155809a2a1a",
      "uuid": "52c7911f-c5b0-45df-b826-3155809a2a1a",
      "@rid": 864,
      "statusId": "success_scheduled",
      "currentActivity": "Device is offline. Configuration template br2_vedge1 scheduled to be attached when device comes online.",
      "actionConfig": "{\"csv-status\":\"complete\",\"csv-deviceId\":\"52c7911f-c5b0-45df-b826-3155809a2a1a\",\"csv-deviceIP\":\"-\",\"csv-host-name\":\"-\",\"csv-templateId\":\"226c0a70-de7b-4a61-9d7e-d3da81c6102e\"}",
      "processId": "push_file_template_configuration-70acb6c7-a589-4a10-be93-27620c46dae5",
      "device-type": "vedge",
      "action": "push_file_template_configuration",
      "deviceModel": "vedge-cloud",
      "startTime": 1554219186805,
      "validity": "valid",
      "requestStatus": "received",
      "status": "Done - Scheduled"
    }
  ],
  "validation": {
    "statusType": "push_file_template_configuration",
    "activity": [
      "[2-Apr-2019 15:33:06 UTC] Starting Checks.",
      "[2-Apr-2019 15:33:06 UTC] Validating if device scheduled for template push are active",
      "[2-Apr-2019 15:33:06 UTC] DeviceIP: -, uuid: 52c7911f-c5b0-45df-b826-3155809a2a1a is not connected to vmanage",
      "[2-Apr-2019 15:33:06 UTC] Sending message to vmanage:10.10.10.10",
      "[2-Apr-2019 15:33:06 UTC] Published messages to vmanage(s)",
      "[2-Apr-2019 15:33:06 UTC] Checks completed."
    ],
    "vmanageIP": "10.10.10.10",
    "system-ip": "Validation",
    "deviceID": "Validation",
    "uuid": "Validation",
    "@rid": 147,
    "statusId": "validation_success",
    "currentActivity": "Done - Validation",
    "actionConfig": "{}",
    "processId": "push_file_template_configuration-70acb6c7-a589-4a10-be93-27620c46dae5",
    "action": "push_file_template_configuration",
    "startTime": 1554219186067,
    "requestStatus": "received",
    "status": "Validation success"
  },
  "summary": {
    "action": "push_file_template_configuration",
    "name": "Push CLI Template Configuration",
    "detailsURL": "/dataservice/device/action/status",
    "startTime": "1554219186606",
    "endTime": "1554219188448",
    "userSessionUserName": "admin",
    "userSessionIP": "10.16.4.81",
    "tenantName": "DefaultTenant",
    "total": 1,
    "status": "done",
    "count": {
      "Done - Scheduled": 1
    }
  },
  "isCancelEnabled": false,
  "isParallelExecutionEnabled": false
}
```

## Create Device Template

**URL:** https://vmanage-ip:port/dataservice/template/device/feature/

**Method:** POST

**POST Request Parameters:**

```json
{
  "templateName": "BR2-CSR-1000v-Template-API",
  "templateDescription": "Branch 2 CSR Template",
  "deviceType": "vedge-CSR-1000v",
  "configType": "template",
  "factoryDefault": false,
  "policyId": "78641b0a-85ad-4f25-9565-849b31ba1c08",
  "featureTemplateUidRange": [],
  "generalTemplates": [
    {
      "templateId": "0441501e-b882-4e62-ac11-be1f6dda70e7",
      "templateType": "aaa"
    },
    {
      "templateId": "76d73e6a-242e-47d2-a798-91f784f52a06",
      "templateType": "bfd-vedge"
    },
    {
      "templateId": "716e9222-d678-4485-bf86-f7f6dcf84323",
      "templateType": "omp-vedge"
    },
    {
      "templateId": "f69d12a2-686f-4de3-b367-59f320b75e5b",
      "templateType": "security-vedge"
    },
    {
      "templateId": "427a4ccf-28a0-4dc8-a07f-7fe4db8f50bd",
      "templateType": "system-vedge",
      "subTemplates": [
        {
          "templateId": "c5b4ba1f-0c7e-499d-b39c-095b9c79d362",
          "templateType": "logging"
        }
      ]
    },
    {
      "templateId": "9d84f2f1-bbbd-4b41-a2c6-2fda5e7c7685",
      "templateType": "vpn-vedge",
      "subTemplates": [
        {
          "templateId": "471aa3d1-9e39-4fbe-b4fc-59c2d2ab6bdd",
          "templateType": "vpn-vedge-interface"
        },
        {
          "templateId": "d877fd68-41c0-4a87-bb09-6d6d444ba92c",
          "templateType": "vpn-vedge-interface"
        }
      ]
    },
    {
      "templateId": "1681b344-d720-4fce-9683-47f55241a347",
      "templateType": "vpn-vedge",
      "subTemplates": [
        {
          "templateId": "8fd27709-2788-4237-80f4-afe0f4221547",
          "templateType": "vpn-vedge-interface"
        }
      ]
    },
    {
      "templateId": "98b03f91-2998-47b5-8bd6-7971486863bf",
      "templateType": "vpn-vedge",
      "subTemplates": [
        {
          "templateId": "d60c22c4-80ef-4ae3-8618-f834dc50a467",
          "templateType": "vpn-vedge-interface"
        }
      ]
    },
    {
      "templateId": "cc7e251e-7402-4d19-a617-0e84d7a5d415",
      "templateType": "virtual-application-utd"
    }
  ],
  "securityPolicyId": "28e3d756-e4bb-4fdf-88f7-6e0fb329c922"
}
```

**Sample Response**

```json
{"templateId":"85c5774c-36a2-46dc-a08a-e816705f366c"}
```

## Create VPN Interface Feature Template

**URL:** https://vmanage-ip:port/dataservice/template/feature/

**Method:** POST

**POST Request Parameters:**

```json
 {
  "templateName": "BR-CSR1000v-VPN512-Interface-Template-API",
  "templateDescription": "BR VPN 512 Interface Template",
  "templateType": "vpn-vedge-interface",
  "deviceType": [
    "vedge-CSR-1000v"
  ],
  "factoryDefault": false,
  "templateMinVersion": "15.0.0",
  "templateDefinition": {
    "if-name": {
      "vipObjectType": "object",
      "vipType": "variableName",
      "vipValue": "",
      "vipVariableName": "mgmt_vpn_if_name"
    },
    "description": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "vpn_if_description"
    },
    "ip": {
      "address": {
        "vipObjectType": "object",
        "vipType": "variableName",
        "vipValue": "",
        "vipVariableName": "mgmt_vpn_if_ipv4_address"
      },
      "secondary-address": {
        "vipType": "ignore",
        "vipValue": [],
        "vipObjectType": "tree",
        "vipPrimaryKey": [
          "address"
        ]
      }
    },
    "dhcp-helper": {
      "vipObjectType": "list",
      "vipType": "ignore",
      "vipVariableName": "vpn_if_dhcp_helper"
    },
    "flow-control": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": "autoneg",
      "vipVariableName": "vpn_if_flow_control"
    },
    "clear-dont-fragment": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": "false",
      "vipVariableName": "vpn_if_clear_dont_fragment"
    },
    "pmtu": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": "false",
      "vipVariableName": "vpn_if_pmtu"
    },
    "mtu": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": 1500,
      "vipVariableName": "vpn_if_ip_mtu"
    },
    "static-ingress-qos": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "vpn_if_static_ingress_qos"
    },
    "tcp-mss-adjust": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "vpn_if_tcp_mss_adjust"
    },
    "mac-address": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "vpn_if_mac_address"
    },
    "speed": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": "_empty",
      "vipVariableName": "vpn_if_speed"
    },
    "duplex": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": "_empty",
      "vipVariableName": "vpn_if_duplex"
    },
    "shutdown": {
      "vipObjectType": "object",
      "vipType": "constant",
      "vipValue": "false",
      "vipVariableName": "vpn_if_shutdown"
    },
    "arp-timeout": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": 1200,
      "vipVariableName": "vpn_if_arp_timeout"
    },
    "autonegotiate": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": "true",
      "vipVariableName": "vpn_if_autonegotiate"
    },
    "shaping-rate": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "qos_shaping_rate"
    },
    "qos-map": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "qos_map"
    },
    "tracker": {
      "vipObjectType": "list",
      "vipType": "ignore",
      "vipVariableName": "vpn_if_tracker"
    },
    "bandwidth-upstream": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "vpn_if_bandwidth_upstream"
    },
    "bandwidth-downstream": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "vpn_if_bandwidth_downstream"
    },
    "block-non-source-ip": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": "false",
      "vipVariableName": "vpn_if_block_non_source_ip"
    },
    "rewrite-rule": {
      "rule-name": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipVariableName": "rewrite_rule_name"
      }
    },
    "tloc-extension": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "vpn_if_tloc_extension"
    },
    "icmp-redirect-disable": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": "false",
      "vipVariableName": "vpn_if_icmp_redirect_disable"
    },
    "tloc-extension-gre-from": {
      "src-ip": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipVariableName": "vpn_if_tloc-ext_gre_from_src_ip"
      },
      "xconnect": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipVariableName": "vpn_if_tloc-ext_gre_from_xconnect"
      }
    },
    "access-list": {
      "vipType": "ignore",
      "vipValue": [],
      "vipObjectType": "tree",
      "vipPrimaryKey": [
        "direction"
      ]
    },
    "policer": {
      "vipType": "ignore",
      "vipValue": [],
      "vipObjectType": "tree",
      "vipPrimaryKey": [
        "policer-name",
        "direction"
      ]
    },
    "ip-directed-broadcast": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": "false",
      "vipVariableName": "vpn_if_ip-directed-broadcast"
    },
    "ipv6": {
      "access-list": {
        "vipType": "ignore",
        "vipValue": [],
        "vipObjectType": "tree",
        "vipPrimaryKey": [
          "direction"
        ]
      },
      "address": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": "",
        "vipVariableName": "vpn_if_ipv6_ipv6_address"
      },
      "dhcp-helper-v6": {
        "vipType": "ignore",
        "vipValue": [],
        "vipObjectType": "tree",
        "vipPrimaryKey": [
          "address"
        ]
      },
      "secondary-address": {
        "vipType": "ignore",
        "vipValue": [],
        "vipObjectType": "tree",
        "vipPrimaryKey": [
          "address"
        ]
      }
    },
    "arp": {
      "ip": {
        "vipType": "ignore",
        "vipValue": [],
        "vipObjectType": "tree",
        "vipPrimaryKey": [
          "addr"
        ]
      }
    },
    "vrrp": {
      "vipType": "ignore",
      "vipValue": [],
      "vipObjectType": "tree",
      "vipPrimaryKey": [
        "grp-id"
      ]
    },
    "ipv6-vrrp": {
      "vipType": "ignore",
      "vipValue": [],
      "vipObjectType": "tree",
      "vipPrimaryKey": [
        "grp-id"
      ]
    },
    "dot1x": {
      "vipType": "ignore",
      "vipObjectType": "node-only"
    }
  }
}
```

**Sample Response:**

```json
{"templateId":"f9dc24e7-568a-42f7-bb94-72de5b72504f"}
```

## Create VPN Feature Template

**URL:** https://vmanage-ip:port/dataservice/template/feature/

**Method:** POST

**POST Request Parameters:**

```json
{
  "templateName": "BR-CSR1000v-VPN512-Template-API",
  "templateDescription": "Branch VPN 512 template",
  "templateType": "vpn-vedge",
  "deviceType": [
    "vedge-CSR-1000v"
  ],
  "factoryDefault": false,
  "templateMinVersion": "15.0.0",
  "templateDefinition": {
    "vpn-id": {
      "vipObjectType": "object",
      "vipType": "constant",
      "vipValue": 512
    },
    "name": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "vpn_name"
    },
    "ecmp-hash-key": {
      "layer4": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": "false",
        "vipVariableName": "vpn_layer4"
      }
    },
    "tcp-optimization": {
      "vipObjectType": "node-only",
      "vipType": "ignore",
      "vipValue": "false",
      "vipVariableName": "vpn_tcp_optimization"
    },
    "nat64": {
      "v4": {
        "pool": {
          "vipType": "ignore",
          "vipValue": [],
          "vipObjectType": "tree",
          "vipPrimaryKey": [
            "name"
          ]
        }
      }
    },
    "host": {
      "vipType": "ignore",
      "vipValue": [],
      "vipObjectType": "tree",
      "vipPrimaryKey": [
        "hostname"
      ]
    },
    "service": {
      "vipType": "ignore",
      "vipValue": [],
      "vipObjectType": "tree",
      "vipPrimaryKey": [
        "svc-type"
      ]
    },
    "ip": {
      "gre-route": {},
      "ipsec-route": {}
    },
    "ipv6": {},
    "omp": {
      "advertise": {
        "vipType": "ignore",
        "vipValue": [],
        "vipObjectType": "tree",
        "vipPrimaryKey": [
          "protocol"
        ]
      },
      "ipv6-advertise": {
        "vipType": "ignore",
        "vipValue": [],
        "vipObjectType": "tree",
        "vipPrimaryKey": [
          "protocol"
        ]
      }
    }
  }
}
```

**Sample Response:**

```json
{"templateId":"8f5cf7c1-4c37-44a9-9205-85d59d0eb555"}
```

## Create VPN 0 Interface

**URL:** https://vmanage-ip:port/dataservice/template/feature/

**Method:** POST

**POST Request Parameters:**

```json
{
  "templateName": "BR-CSR1000-VPN0-MPLS-Interface-API",
  "templateDescription": "CSR1000v VPN0 MPLS interface",
  "templateType": "vpn-vedge-interface",
  "deviceType": [
    "vedge-CSR-1000v"
  ],
  "factoryDefault": false,
  "templateMinVersion": "15.0.0",
  "templateDefinition": {
    "if-name": {
      "vipObjectType": "object",
      "vipType": "variableName",
      "vipValue": "",
      "vipVariableName": "mpls_vpn_if_name"
    },
    "description": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "vpn_if_description"
    },
    "ip": {
      "address": {
        "vipObjectType": "object",
        "vipType": "variableName",
        "vipValue": "",
        "vipVariableName": "mpls_vpn_if_ipv4_address"
      },
      "secondary-address": {
        "vipType": "ignore",
        "vipValue": [],
        "vipObjectType": "tree",
        "vipPrimaryKey": [
          "address"
        ]
      }
    },
    "dhcp-helper": {
      "vipObjectType": "list",
      "vipType": "ignore",
      "vipVariableName": "vpn_if_dhcp_helper"
    },
    "flow-control": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": "autoneg",
      "vipVariableName": "vpn_if_flow_control"
    },
    "clear-dont-fragment": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": "false",
      "vipVariableName": "vpn_if_clear_dont_fragment"
    },
    "pmtu": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": "false",
      "vipVariableName": "vpn_if_pmtu"
    },
    "mtu": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": 1500,
      "vipVariableName": "vpn_if_ip_mtu"
    },
    "static-ingress-qos": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "vpn_if_static_ingress_qos"
    },
    "tcp-mss-adjust": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "vpn_if_tcp_mss_adjust"
    },
    "mac-address": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "vpn_if_mac_address"
    },
    "speed": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": "_empty",
      "vipVariableName": "vpn_if_speed"
    },
    "duplex": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": "_empty",
      "vipVariableName": "vpn_if_duplex"
    },
    "shutdown": {
      "vipObjectType": "object",
      "vipType": "constant",
      "vipValue": "false",
      "vipVariableName": "vpn_if_shutdown"
    },
    "arp-timeout": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": 1200,
      "vipVariableName": "vpn_if_arp_timeout"
    },
    "autonegotiate": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": "true",
      "vipVariableName": "vpn_if_autonegotiate"
    },
    "shaping-rate": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "qos_shaping_rate"
    },
    "qos-map": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "qos_map"
    },
    "tracker": {
      "vipObjectType": "list",
      "vipType": "ignore",
      "vipVariableName": "vpn_if_tracker"
    },
    "bandwidth-upstream": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "vpn_if_bandwidth_upstream"
    },
    "bandwidth-downstream": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "vpn_if_bandwidth_downstream"
    },
    "block-non-source-ip": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": "false",
      "vipVariableName": "vpn_if_block_non_source_ip"
    },
    "rewrite-rule": {
      "rule-name": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipVariableName": "rewrite_rule_name"
      }
    },
    "tloc-extension": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipVariableName": "vpn_if_tloc_extension"
    },
    "icmp-redirect-disable": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": "false",
      "vipVariableName": "vpn_if_icmp_redirect_disable"
    },
    "tloc-extension-gre-from": {
      "src-ip": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipVariableName": "vpn_if_tloc-ext_gre_from_src_ip"
      },
      "xconnect": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipVariableName": "vpn_if_tloc-ext_gre_from_xconnect"
      }
    },
    "access-list": {
      "vipType": "ignore",
      "vipValue": [],
      "vipObjectType": "tree",
      "vipPrimaryKey": [
        "direction"
      ]
    },
    "policer": {
      "vipType": "ignore",
      "vipValue": [],
      "vipObjectType": "tree",
      "vipPrimaryKey": [
        "policer-name",
        "direction"
      ]
    },
    "tunnel-interface": {
      "encapsulation": {
        "vipType": "constant",
        "vipValue": [
          {
            "preference": {
              "vipObjectType": "object",
              "vipType": "ignore",
              "vipVariableName": "vpn_if_tunnel_ipsec_preference"
            },
            "weight": {
              "vipObjectType": "object",
              "vipType": "ignore",
              "vipValue": 1,
              "vipVariableName": "vpn_if_tunnel_ipsec_weight"
            },
            "encap": {
              "vipType": "constant",
              "vipValue": "ipsec",
              "vipObjectType": "object"
            },
            "priority-order": [
              "encap",
              "preference",
              "weight"
            ]
          }
        ],
        "vipObjectType": "tree",
        "vipPrimaryKey": [
          "encap"
        ]
      },
      "group": {
        "vipObjectType": "list",
        "vipType": "ignore",
        "vipVariableName": "vpn_if_tunnel_group"
      },
      "border": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": "false",
        "vipVariableName": "vpn_if_tunnel_border"
      },
      "color": {
        "value": {
          "vipObjectType": "object",
          "vipType": "constant",
          "vipValue": "mpls",
          "vipVariableName": "vpn_if_tunnel_color_value"
        },
        "restrict": {
          "vipObjectType": "node-only",
          "vipType": "ignore",
          "vipValue": "false",
          "vipVariableName": "vpn_if_tunnel_color_restrict"
        }
      },
      "carrier": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": "default",
        "vipVariableName": "vpn_if_tunnel_carrier"
      },
      "bind": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipVariableName": "vpn_if_tunnel_bind"
      },
      "allow-service": {
        "dhcp": {
          "vipObjectType": "object",
          "vipType": "ignore",
          "vipValue": "true",
          "vipVariableName": "vpn_if_tunnel_dhcp"
        },
        "dns": {
          "vipObjectType": "object",
          "vipType": "ignore",
          "vipValue": "true",
          "vipVariableName": "vpn_if_tunnel_dns"
        },
        "icmp": {
          "vipObjectType": "object",
          "vipType": "ignore",
          "vipValue": "true",
          "vipVariableName": "vpn_if_tunnel_icmp"
        },
        "sshd": {
          "vipObjectType": "object",
          "vipType": "ignore",
          "vipValue": "false",
          "vipVariableName": "vpn_if_tunnel_sshd"
        },
        "ntp": {
          "vipObjectType": "object",
          "vipType": "ignore",
          "vipValue": "false",
          "vipVariableName": "vpn_if_tunnel_ntp"
        },
        "stun": {
          "vipObjectType": "object",
          "vipType": "constant",
          "vipValue": "true",
          "vipVariableName": "vpn_if_tunnel_stun"
        },
        "all": {
          "vipObjectType": "object",
          "vipType": "ignore",
          "vipValue": "false",
          "vipVariableName": "vpn_if_tunnel_all"
        },
        "bgp": {
          "vipObjectType": "object",
          "vipType": "ignore",
          "vipValue": "false",
          "vipVariableName": "vpn_if_tunnel_bgp"
        },
        "ospf": {
          "vipObjectType": "object",
          "vipType": "ignore",
          "vipValue": "false",
          "vipVariableName": "vpn_if_tunnel_ospf"
        },
        "netconf": {
          "vipObjectType": "object",
          "vipType": "ignore",
          "vipValue": "false",
          "vipVariableName": "vpn_if_tunnel_netconf"
        },
        "snmp": {
          "vipObjectType": "object",
          "vipType": "ignore",
          "vipValue": "false",
          "vipVariableName": "vpn_if_tunnel_snmp"
        },
        "https": {
          "vipObjectType": "object",
          "vipType": "ignore",
          "vipValue": "true",
          "vipVariableName": "vpn_if_tunnel_https"
        }
      },
      "max-control-connections": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipVariableName": "vpn_if_tunnel_max_control_connections"
      },
      "vbond-as-stun-server": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": "false",
        "vipVariableName": "vpn_if_tunnel_vbond_as_stun_server"
      },
      "exclude-controller-group-list": {
        "vipObjectType": "list",
        "vipType": "ignore",
        "vipVariableName": "vpn_if_tunnel_exclude_controller_group_list"
      },
      "vmanage-connection-preference": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": 5,
        "vipVariableName": "vpn_if_tunnel_vmanage_connection_preference"
      },
      "port-hop": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": "true",
        "vipVariableName": "vpn_if_tunnel_port_hop"
      },
      "low-bandwidth-link": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": "false",
        "vipVariableName": "vpn_if_tunnel_low_bandwidth_link"
      },
      "last-resort-circuit": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": "false",
        "vipVariableName": "vpn_if_tunnel_last_resort_circuit"
      },
      "hold-time": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": 7000,
        "vipVariableName": "hold-time"
      },
      "nat-refresh-interval": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": 5,
        "vipVariableName": "vpn_if_tunnel_nat_refresh_interval"
      },
      "hello-interval": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": 1000,
        "vipVariableName": "vpn_if_tunnel_hello_interval"
      },
      "hello-tolerance": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": 12,
        "vipVariableName": "vpn_if_tunnel_hello_tolerance"
      },
      "tloc-extension-gre-to": {
        "dst-ip": {
          "vipObjectType": "object",
          "vipType": "ignore",
          "vipVariableName": "vpn_if_tunnel_tloc_ext_gre_to_dst_ip"
        }
      },
      "control-connections": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": "true",
        "vipVariableName": "control_connections"
      }
    },
    "ip-directed-broadcast": {
      "vipObjectType": "object",
      "vipType": "ignore",
      "vipValue": "false",
      "vipVariableName": "vpn_if_ip-directed-broadcast"
    },
    "ipv6": {
      "access-list": {
        "vipType": "ignore",
        "vipValue": [],
        "vipObjectType": "tree",
        "vipPrimaryKey": [
          "direction"
        ]
      },
      "address": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": "",
        "vipVariableName": "vpn_if_ipv6_ipv6_address"
      },
      "dhcp-helper-v6": {
        "vipType": "ignore",
        "vipValue": [],
        "vipObjectType": "tree",
        "vipPrimaryKey": [
          "address"
        ]
      },
      "secondary-address": {
        "vipType": "ignore",
        "vipValue": [],
        "vipObjectType": "tree",
        "vipPrimaryKey": [
          "address"
        ]
      }
    },
    "arp": {
      "ip": {
        "vipType": "ignore",
        "vipValue": [],
        "vipObjectType": "tree",
        "vipPrimaryKey": [
          "addr"
        ]
      }
    },
    "vrrp": {
      "vipType": "ignore",
      "vipValue": [],
      "vipObjectType": "tree",
      "vipPrimaryKey": [
        "grp-id"
      ]
    },
    "ipv6-vrrp": {
      "vipType": "ignore",
      "vipValue": [],
      "vipObjectType": "tree",
      "vipPrimaryKey": [
        "grp-id"
      ]
    },
    "dot1x": {
      "vipType": "ignore",
      "vipObjectType": "node-only"
    }
  }
}
```

**Sample Response**

```json
{"templateId":"e6bed889-fb53-4c39-8188-7c3ce409b916"}
```

## Attach Device Template

**URL:** https://vmanage-ip:port/dataservice/template/device/config/attachfeature

**Method:** POST

**POST Request Parameters:**

```json
{
  "deviceTemplateList": [
    {
      "templateId": "659b36ec-04f5-45cb-b6b0-c350f84568d1",
      "device": [
        {
          "csv-status": "complete",
          "csv-deviceId": "CSR-c30a74a6-bacf-4194-bfd3-8bc85081e16c",
          "csv-deviceIP": "1.1.1.5",
          "csv-host-name": "BR1-CSR1000v",
          "/10/vpn_10_if_name/interface/if-name": "GigabitEthernet4",
          "/10/vpn_10_if_name/interface/ip/address": "192.168.60.1/24",
          "/512/mgmt_vpn_if_name/interface/if-name": "GigabitEthernet3",
          "/512/mgmt_vpn_if_name/interface/ip/address": "192.168.10.5/24",
          "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/mpls_vpn_next_hop_ip_address_0/address": "20.20.20.1",
          "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/internet_vpn_next_hop_ip_address_1/address": "40.40.40.1",
          "/0/Internet_vpn_if_name/interface/if-name": "GigabitEthernet2",
          "/0/Internet_vpn_if_name/interface/ip/address": "40.40.40.2/24",
          "/0/mpls_vpn_if_name/interface/if-name": "GigabitEthernet1",
          "/0/mpls_vpn_if_name/interface/ip/address": "20.20.20.2/24",
          "//system/host-name": "BR1-CSR1000v",
          "//system/system-ip": "1.1.1.5",
          "//system/site-id": "200",
          "csv-templateId": "659b36ec-04f5-45cb-b6b0-c350f84568d1"
        }
      ],
      "isEdited": false,
      "isMasterEdited": false
    }
  ]
}
```

**Sample Response:**

```json
{"id":"push_feature_template_configuration-d75b2879-9f85-4045-a59b-19f34f62041c"}
```

monitor status using GET Request on below URL

**URL:** https://vmanage-ip:port/dataservice/device/action/status/push_feature_template_configuration-d75b2879-9f85-4045-a59b-19f34f62041c

**Sample Response:**

```json
  "data": [
    {
      "local-system-ip": "1.1.1.5",
      "statusType": "push_feature_template_configuration",
      "activity": [
        "[2-Jun-2019 23:14:32 UTC] Configuring device with feature template: BR1-CSR-1000v-AMP",
        "[2-Jun-2019 23:14:32 UTC] Generating configuration from template",
        "[2-Jun-2019 23:14:37 UTC] Checking and creating device in vManage",
        "[2-Jun-2019 23:14:37 UTC] Device is online",
        "[2-Jun-2019 23:14:37 UTC] Updating device configuration in vManage",
        "[2-Jun-2019 23:14:41 UTC] Pushing configuration to device",
        "[2-Jun-2019 23:14:49 UTC] Template successfully attached to device"
      ],
      "vmanageIP": "1.1.1.2",
      "system-ip": "1.1.1.5",
      "host-name": "BR1-CSR1000v",
      "site-id": "200",
      "deviceID": "CSR-c30a74a6-bacf-4194-bfd3-8bc85081e16c",
      "uuid": "CSR-c30a74a6-bacf-4194-bfd3-8bc85081e16c",
      "@rid": 1544,
      "statusId": "success",
      "currentActivity": "Done - Push Feature Template Configuration",
      "actionConfig": "{\"csv-status\":\"complete\",\"csv-deviceId\":\"CSR-c30a74a6-bacf-4194-bfd3-8bc85081e16c\",\"csv-deviceIP\":\"1.1.1.5\",\"csv-host-name\":\"BR1-CSR1000v\",\"/10/vpn_10_if_name/interface/if-name\":\"GigabitEthernet4\",\"/10/vpn_10_if_name/interface/ip/address\":\"192.168.60.1/24\",\"/512/mgmt_vpn_if_name/interface/if-name\":\"GigabitEthernet3\",\"/512/mgmt_vpn_if_name/interface/ip/address\":\"192.168.10.5/24\",\"/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/mpls_vpn_next_hop_ip_address_0/address\":\"20.20.20.1\",\"/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/internet_vpn_next_hop_ip_address_1/address\":\"40.40.40.1\",\"/0/Internet_vpn_if_name/interface/if-name\":\"GigabitEthernet2\",\"/0/Internet_vpn_if_name/interface/ip/address\":\"40.40.40.2/24\",\"/0/mpls_vpn_if_name/interface/if-name\":\"GigabitEthernet1\",\"/0/mpls_vpn_if_name/interface/ip/address\":\"20.20.20.2/24\",\"//system/host-name\":\"BR1-CSR1000v\",\"//system/system-ip\":\"1.1.1.5\",\"//system/site-id\":\"200\",\"csv-templateId\":\"659b36ec-04f5-45cb-b6b0-c350f84568d1\"}",
      "processId": "push_feature_template_configuration-d75b2879-9f85-4045-a59b-19f34f62041c",
      "device-type": "vedge",
      "action": "push_feature_template_configuration",
      "deviceModel": "vedge-CSR-1000v",
      "startTime": 1559517272806,
      "validity": "valid",
      "requestStatus": "received",
      "status": "Success"
    }
  ],
  "validation": {
    "statusType": "push_feature_template_configuration",
    "activity": [
      "[2-Jun-2019 23:14:32 UTC] Starting Checks.",
      "[2-Jun-2019 23:14:32 UTC] Validating if device scheduled for template push are active",
      "[2-Jun-2019 23:14:32 UTC] Sending message to vmanage:1.1.1.2",
      "[2-Jun-2019 23:14:32 UTC] Published messages to vmanage(s)",
      "[2-Jun-2019 23:14:32 UTC] Checks completed."
    ],
    "vmanageIP": "1.1.1.2",
    "system-ip": "Validation",
    "deviceID": "Validation",
    "uuid": "Validation",
    "@rid": 1562,
    "statusId": "validation_success",
    "currentActivity": "Done - Validation",
    "actionConfig": "{}",
    "processId": "push_feature_template_configuration-d75b2879-9f85-4045-a59b-19f34f62041c",
    "action": "push_feature_template_configuration",
    "startTime": 1559517272576,
    "requestStatus": "received",
    "status": "Validation success"
  },
  "summary": {
    "action": "push_feature_template_configuration",
    "name": "Push Feature Template Configuration",
    "detailsURL": "/dataservice/device/action/status",
    "startTime": "1559517272717",
    "endTime": "1559517289806",
    "userSessionUserName": "admin",
    "userSessionIP": "10.142.84.61",
    "tenantName": "DefaultTenant",
    "total": 1,
    "status": "done",
    "count": {
      "Success": 1
    }
  },
```
