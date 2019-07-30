Table of Contents
=================

   * [Create vManage local user](#create-vmanage-local-user)
   * [Delete vManage local user](#delete-vmanage-local-user)
   * [Edit vEdge password via Template](#edit-vedge-password-via-template)
   * [Push Template Change](#push-template-change)
   * [Fetching list of device templates](#fetching-list-of-device-templates)
   * [Fetching Devices attached](#fetching-devices-attached)
   * [Attach Template to Device](#attach-template-to-device)
   * [Monitor Template Push Operation](#monitor-template-push-operation)
   * [References](#references)

# Create vManage local user

**Resource URL:** `https://<vmanage-ip>/dataservice/admin/user`

**Method:** POST

**JSON Payload:** Below sample payload creates netadmin group user account with username/password:vmanageadmin/vmanageadmin.

```json
{"group":["netadmin"],
 "description":"vManage-admin",
 "userName":"vmanageadmin",
 "password":"vmanageadmin"}
```

**Output on vManage Device CLI after configuration:**

vmanage# show running-config system aaa
<snip>
  user vmanageadmin
   password    <Hashed-Value>
   description vManage-admin
   group       netadmin


# Delete vManage local user

**Resource URL:** `https://<vmanage-ip>/dataservice/admin/user/<username to be deleted>`

**Method:** DELETE


# Edit vEdge password via Template

GET list of templates and its UUID value. 

**Resource URL:** `https://<vmanage-ip>/dataservice/template/feature`

**Method:** GET

Add new local user in AAA Template: 

**Resource URL:** `https://<vmanage-ip>/dataservice/template/feature/<template-uuid>`

**Method:** PUT

**Json Payload:**

```json
{
  "templateName": "vEdge-AAA-API-Call",
  "templateDescription": "vEdge-AAA-API-Call",
  "templateType": "aaa",
  "templateMinVersion": "15.0.0",
  "templateDefinition": {
    "aaa": {
      "auth-order": {
        "vipType": "constant",
        "vipValue": [
          {
            "vipType": "constant",
            "vipValue": "local",
            "vipObjectType": "object"
          },
          {
            "vipType": "constant",
            "vipValue": "radius",
            "vipObjectType": "object"
          },
          {
            "vipType": "constant",
            "vipValue": "tacacs",
            "vipObjectType": "object"
          }
        ],
        "vipObjectType": "list",
        "vipVariableName": "auth_order"
      },
      "auth-fallback": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": "false",
        "vipVariableName": "auth_fallback"
      },
      "admin-auth-order": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": "false",
        "vipVariableName": "admin_auth_order"
      },
      "logs": {
        "audit-disable": {
          "vipObjectType": "object",
          "vipType": "ignore",
          "vipValue": "false",
          "vipVariableName": "disable_audit_logs"
        },
        "netconf-disable": {
          "vipObjectType": "object",
          "vipType": "ignore",
          "vipValue": "false",
          "vipVariableName": "disable_netconf_logs"
        }
      },
      "radius-servers": {
        "vipObjectType": "list",
        "vipType": "ignore",
        "vipValue": [
          ""
        ],
        "vipVariableName": "radius_servers"
      },
      "usergroup": {
        "vipType": "constant",
        "vipValue": [
          {
            "name": {
              "vipObjectType": "object",
              "vipType": "constant",
              "vipValue": "netadmin"
            },
            "viewMode": "view",
            "priority-order": [
              "name"
            ]
          },
          {
            "name": {
              "vipObjectType": "object",
              "vipType": "constant",
              "vipValue": "basic"
            },
            "priority-order": [
              "name",
              "task"
            ],
            "task": {
              "vipType": "constant",
              "vipValue": [
                {
                  "mode": {
                    "vipType": "constant",
                    "vipValue": "system",
                    "vipObjectType": "object"
                  },
                  "permission": {
                    "vipType": "constant",
                    "vipValue": [
                      {
                        "vipType": "constant",
                        "vipValue": "read",
                        "vipObjectType": "object"
                      },
                      {
                        "vipType": "constant",
                        "vipValue": "write",
                        "vipObjectType": "object"
                      }
                    ],
                    "vipObjectType": "list"
                  },
                  "priority-order": [
                    "mode",
                    "permission"
                  ]
                },
                {
                  "mode": {
                    "vipType": "constant",
                    "vipValue": "interface",
                    "vipObjectType": "object"
                  },
                  "permission": {
                    "vipType": "constant",
                    "vipValue": [
                      {
                        "vipType": "constant",
                        "vipValue": "read",
                        "vipObjectType": "object"
                      },
                      {
                        "vipType": "constant",
                        "vipValue": "write",
                        "vipObjectType": "object"
                      }
                    ],
                    "vipObjectType": "list"
                  },
                  "priority-order": [
                    "mode",
                    "permission"
                  ]
                }
              ],
              "vipObjectType": "tree",
              "vipPrimaryKey": [
                "mode"
              ]
            }
          },
          {
            "name": {
              "vipObjectType": "object",
              "vipType": "constant",
              "vipValue": "operator"
            },
            "priority-order": [
              "name",
              "task"
            ],
            "task": {
              "vipType": "constant",
              "vipValue": [
                {
                  "mode": {
                    "vipType": "constant",
                    "vipValue": "system",
                    "vipObjectType": "object"
                  },
                  "permission": {
                    "vipType": "constant",
                    "vipValue": [
                      {
                        "vipType": "constant",
                        "vipValue": "read",
                        "vipObjectType": "object"
                      }
                    ],
                    "vipObjectType": "list"
                  },
                  "priority-order": [
                    "mode",
                    "permission"
                  ]
                },
                {
                  "mode": {
                    "vipType": "constant",
                    "vipValue": "interface",
                    "vipObjectType": "object"
                  },
                  "permission": {
                    "vipType": "constant",
                    "vipValue": [
                      {
                        "vipType": "constant",
                        "vipValue": "read",
                        "vipObjectType": "object"
                      }
                    ],
                    "vipObjectType": "list"
                  },
                  "priority-order": [
                    "mode",
                    "permission"
                  ]
                },
                {
                  "mode": {
                    "vipType": "constant",
                    "vipValue": "policy",
                    "vipObjectType": "object"
                  },
                  "permission": {
                    "vipType": "constant",
                    "vipValue": [
                      {
                        "vipType": "constant",
                        "vipValue": "read",
                        "vipObjectType": "object"
                      }
                    ],
                    "vipObjectType": "list"
                  },
                  "priority-order": [
                    "mode",
                    "permission"
                  ]
                },
                {
                  "mode": {
                    "vipType": "constant",
                    "vipValue": "routing",
                    "vipObjectType": "object"
                  },
                  "permission": {
                    "vipType": "constant",
                    "vipValue": [
                      {
                        "vipType": "constant",
                        "vipValue": "read",
                        "vipObjectType": "object"
                      }
                    ],
                    "vipObjectType": "list"
                  },
                  "priority-order": [
                    "mode",
                    "permission"
                  ]
                },
                {
                  "mode": {
                    "vipType": "constant",
                    "vipValue": "security",
                    "vipObjectType": "object"
                  },
                  "permission": {
                    "vipType": "constant",
                    "vipValue": [
                      {
                        "vipType": "constant",
                        "vipValue": "read",
                        "vipObjectType": "object"
                      }
                    ],
                    "vipObjectType": "list"
                  },
                  "priority-order": [
                    "mode",
                    "permission"
                  ]
                }
              ],
              "vipObjectType": "tree",
              "vipPrimaryKey": [
                "mode"
              ]
            }
          }
        ],
        "vipObjectType": "tree",
        "vipPrimaryKey": [
          "name"
        ]
      },
      "user": {
        "vipType": "constant",
        "vipValue": [
          {
            "vipOptional": false,
            "name": {
              "vipObjectType": "object",
              "vipType": "constant",
              "vipValue": "<username>",
              "vipVariableName": "user_name_0"
            },
            "password": {
              "vipObjectType": "object",
              "vipType": "constant",
              "vipValue": "<plain-text-password>"
            },
            "description": {
              "vipObjectType": "object",
              "vipType": "ignore",
              "vipValue": ""
            },
            "group": {
              "vipType": "constant",
              "vipValue": [],
              "vipObjectType": "list"
            },
            "priority-order": [
              "name",
              "password",
              "secret",
              "description",
              "group"
            ]
          },
          {
            "name": {
              "vipObjectType": "object",
              "vipType": "constant",
              "vipValue": "<username>",
              "vipVariableName": "user_name"
            },
            "password": {
              "vipObjectType": "object",
              "vipType": "constant",
              "vipValue": "<plain-text-password>"
            },
            "description": {
              "vipObjectType": "object",
              "vipType": "constant",
              "vipValue": "<user-description>",
              "vipVariableName": "user_description"
            },
            "group": {
              "vipType": "constant",
              "vipValue": [
                {
                  "vipType": "constant",
                  "vipValue": "netadmin",
                  "vipObjectType": "object"
                }
              ],
              "vipObjectType": "list",
              "vipVariableName": "user_group"
            },
            "priority-order": [
              "name",
              "password",
              "secret",
              "description",
              "group"
            ]
          }
        ],
        "vipObjectType": "tree",
        "vipPrimaryKey": [
          "name"
        ]
      }
    },
    "tacacs": {
      "timeout": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": 5,
        "vipVariableName": "tacacs_timeout"
      },
      "authentication": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": "pap",
        "vipVariableName": "tacacs_authentication"
      }
    },
    "radius": {
      "timeout": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": 5,
        "vipVariableName": "radius_timeout"
      },
      "retransmit": {
        "vipObjectType": "object",
        "vipType": "ignore",
        "vipValue": 3,
        "vipVariableName": "retransmit"
      }
    }
  },
  "transitionInProgress": true,
  "userGroupName": {
    "key": "name",
    "description": "Name",
    "details": "Set name of user group",
    "optionType": [
      {
        "value": "constant",
        "display": "Global",
        "iconClass": "language",
        "iconColor": "icon-global"
      }
    ],
    "originalDefaultOption": "constant",
    "defaultOption": "constant",
    "dataType": {
      "type": "string",
      "minLength": 1,
      "maxLength": 128
    },
    "dataPath": [],
    "vipObjectType": "object",
    "objectType": "object",
    "deleteFlag": true
  },
  "viewMode": "add",
  "deviceType": [
    "vedge-cloud"
  ],
  "deviceModels": [
    {
      "name": "vedge-cloud",
      "displayName": "vEdge Cloud",
      "deviceType": "vedge",
      "isCliSupported": true,
      "isCiscoDeviceModel": false
    }
  ],
  "templateUrl": "/app/configuration/template/feature/templates/aaa-15.0.0.html",
  "factoryDefault": false
}
```

# Push Template Change

After editing the AAA feature template, we need to initiate the template push process by sending below POST Request. 

**Resource URL:** `https://<vmanage-ip>/dataservice/template/device/config/input/`

**Method:** POST

**Payload** (Please see below sections Fetching list of device templates and Fetching Devices attached)

```
{"templateId":"<Device Feature Template ID>",
 "deviceIds":["<UUID of device attached with this template>"],
 "isEdited":true,
 "isMasterEdited":false}
```

**Sample Response**

```
  "data": [
    {
      "csv-status": "complete",
      "csv-deviceId": "4ea1260d-3a3f-479b-bfaa-9bd3181bbdd5",
      "csv-deviceIP": "1.1.1.8",
      "csv-host-name": "BR-3-vEdge",
      "/10/vpn_10_if_name/interface/if-name": "ge0/1",
      "/10/vpn_10_if_name/interface/ip/address": "<removed-ip-address>",
      "/512/VPN512_Interface/interface/if-name": "eth0",
      "/512/VPN512_Interface/interface/ip/address": "<removed-ip-address>",
      "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/MPLS-GW/address": "<removed-ip-address>",
      "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/Internet-GW/address": "<removed-ip-address>",
      "/0/Internet_if_name/interface/if-name": "ge0/0",
      "/0/Internet_if_name/interface/ip/address": "<removed-ip-address>",
      "/0/MPLS_if_name/interface/if-name": "ge0/2",
      "/0/MPLS_if_name/interface/ip/address": "<removed-ip-address>",
      "//system/host-name": "BR-3-vEdge",
      "//system/system-ip": "1.1.1.8",
      "//system/site-id": "500"
    }
 ```

# Fetching list of device templates

**Resource URL:** `https://<vmanage-ip>/dataservice/template/device`

**Method:** GET

**Sample Response:**

```
  "data": [
    {
      "deviceType": "vedge-cloud",
      "lastUpdatedBy": "admin",
      "factoryDefault": false,
      "templateName": "BR-3-vEdge",
      "devicesAttached": 1,
      "templateDescription": "Branch 3 vEdge",
      "lastUpdatedOn": 1564482763586,
      "configType": "template",
      "templateId": "becb0602-7229-471c-80d3-b0ae23513a61",
      "templateAttached": 13
    },
```

# Fetching Devices attached 

**Resource URL:** `https://<vmanage-ip>/dataservice/template/device/config/attached/<template-id>`

**Method:** GET

**Sample Response:**

```
  "data": [
    {
      "host-name": "BR-3-vEdge",
      "deviceIP": "1.1.1.8",
      "local-system-ip": "1.1.1.8",
      "site-id": "500",
      "device-groups": [
        "No groups"
      ],
      "uuid": "4ea1260d-3a3f-479b-bfaa-9bd3181bbdd5",
      "personality": "vedge",
      "configCloudxMode": "dia"
    }
 ```

# Attach Template to Device

**Resource URL:** `https://<vmanage-ip>/dataservice/template/device/config/attachfeature`

**Method:** POST

**Sample Payload**

```
{
  "deviceTemplateList": [
    {
      "templateId": "becb0602-7229-471c-80d3-b0ae23513a61",
      "device": [
        {
          "csv-status": "complete",
          "csv-deviceId": "4ea1260d-3a3f-479b-bfaa-9bd3181bbdd5",
          "csv-deviceIP": "1.1.1.8",
          "csv-host-name": "BR-3-vEdge",
          "/10/vpn_10_if_name/interface/if-name": "ge0/1",
          "/10/vpn_10_if_name/interface/ip/address": "192.168.50.1/24",
          "/512/VPN512_Interface/interface/if-name": "eth0",
          "/512/VPN512_Interface/interface/ip/address": "192.168.10.8/24",
          "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/MPLS-GW/address": "80.80.80.1",
          "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/Internet-GW/address": "90.90.90.1",
          "/0/Internet_if_name/interface/if-name": "ge0/0",
          "/0/Internet_if_name/interface/ip/address": "90.90.90.2/24",
          "/0/MPLS_if_name/interface/if-name": "ge0/2",
          "/0/MPLS_if_name/interface/ip/address": "80.80.80.2/24",
          "//system/host-name": "BR-3-vEdge",
          "//system/system-ip": "1.1.1.8",
          "//system/site-id": "500",
          "csv-templateId": "becb0602-7229-471c-80d3-b0ae23513a61"
        }
      ],
      "isEdited": true,
      "isMasterEdited": false
    }
  ]
}
```

**Sample Response**

```
{"id":"push_feature_template_configuration-d8a5bbec-7514-4956-ae58-a5debcfc8140"}
```

# Monitor Template Push Operation

**Resource URL** `https://<vmanage-ip>/dataservice/device/action/status/push_feature_template_configuration-d8a5bbec-7514-4956-ae58-a5debcfc8140` (push id is response to above POST request)

**Method:** GET

**Sample Response:**

```
  "summary": {
    "action": "push_feature_template_configuration",
    "name": "Push Feature Template Configuration",
    "detailsURL": "/dataservice/device/action/status",
    "startTime": "1564483317714",
    "endTime": "0",
    "userSessionUserName": "admin",
    "userSessionIP": "10.232.13.25",
    "tenantName": "DefaultTenant",
    "total": 1,
    "status": "in_progress",       (# status value changes to "done" on completing the template push to devices)
    "count": {
      "In progress": 1
    }
```

# References

Sections **Fetching Device csv values** and **Attaching new Device template** in below code.

https://github.com/suchandanreddy/sdwan-umbrella-policy/blob/master/configure-umbrella-policy.py