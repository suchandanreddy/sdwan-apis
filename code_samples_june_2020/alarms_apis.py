#! /usr/bin/env python

import requests
import sys
import json
import os
import click
import tabulate
import cmd
import datetime
import pytz

from requests.packages.urllib3.exceptions import InsecureRequestWarning

vmanage_host = os.environ.get("vmanage_host")
vmanage_port = os.environ.get("vmanage_port")
vmanage_username = os.environ.get("vmanage_username")
vmanage_password = os.environ.get("vmanage_password")

if vmanage_host is None or vmanage_port is None or vmanage_username is None or vmanage_password is None:
    print("For Windows Workstation, vManage details must be set via environment variables using below commands")
    print("set vmanage_host=198.18.1.10")
    print("set vmanage_port=443")
    print("set vmanage_username=admin")
    print("set vmanage_password=admin")
    print("For MAC OSX Workstation, vManage details must be set via environment variables using below commands")
    print("export vmanage_host=198.18.1.10")
    print("export vmanage_port=443")
    print("export vmanage_username=admin")
    print("export vmanage_password=admin")
    exit()

requests.packages.urllib3.disable_warnings()

class Authentication:

    @staticmethod
    def get_jsessionid(vmanage_host, vmanage_port, username, password):
        api = "/j_security_check"
        base_url = "https://%s:%s"%(vmanage_host, vmanage_port)
        url = base_url + api
        payload = {'j_username' : username, 'j_password' : password}
        
        response = requests.post(url=url, data=payload, verify=False)
        try:
            cookies = response.headers["Set-Cookie"]
            jsessionid = cookies.split(";")
            return(jsessionid[0])
        except:
            print(response.text)
            exit()
       
    @staticmethod
    def get_token(vmanage_host, vmanage_port, jsessionid):
        headers = {'Cookie': jsessionid}
        base_url = "https://%s:%s"%(vmanage_host, vmanage_port)
        api = "/dataservice/client/token"
        url = base_url + api      
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return(response.text)
        else:
            return None

Auth = Authentication()
jsessionid = Auth.get_jsessionid(vmanage_host,vmanage_port,vmanage_username,vmanage_password)
token = Auth.get_token(vmanage_host,vmanage_port,jsessionid)

if token is not None:
    header = {'Content-Type': "application/json",'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
else:
    header = {'Content-Type': "application/json",'Cookie': jsessionid}

base_url = "https://%s:%s/dataservice"%(vmanage_host, vmanage_port)

@click.group()
def cli():
    """Command line tool for deploying templates to CISCO SDWAN.
    """
    pass

@click.command()
def list_alarms_tags():
    """ Retrieve list of alarm tags.                                       
        \nExample command: ./alarms_apis.py list-alarms-tags
    """
    click.secho("\nRetrieving the alarm tags\n")

    url = base_url + "/alarms/rulenamedisplay/keyvalue"

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        click.echo("Failed to get list of devices " + str(response.text))
        exit()

    tags = list()
    cli = cmd.Cmd()

    for item in items:
        if item['key'] == "":
            continue
        tags.append(item['key'])

    click.echo(cli.columnize(tags,displaywidth=120))

@click.command()
@click.option("--alarm_tag", help="Alarm tag name")
def list_alarms(alarm_tag):
    """ Retrieve list of alarms related to provided tag.
        \nExample command: ./alarms_apis.py list-alarms --alarm_tag OMP_Site_Up
    """
    click.echo("\nRetrieving the alarms with tag %s\n"%alarm_tag)

    url = base_url + "/alarms"

    query = {
                "query": {
                    "condition": "AND",         # Logical AND Operation among rules defined below
                    "rules": [
                    {
                        "value": [              # last 24 hours
                            "24"
                        ],
                        "field": "entry_time",
                        "type": "date",
                        "operator": "last_n_hours"
                    },
                    {
                        "value": [              # Return both active and cleared alarms
                        "false","true"
                        ],
                        "field": "active",
                        "type": "string",
                        "operator": "in"
                    },
                    {
                        "value": [              # Alarm tag to filter specific type of alarms
                        alarm_tag
                        ],
                        "field": "rule_name_display",
                        "type": "string",
                        "operator": "in"
                    },
                    {
                        "value":[              
                            "false",
                        ],
                        "field": "acknowledged",
                        "type": "string",
                        "operator": "in"
                    }
                    ]
                }           
            }

    response = requests.post(url=url, headers=header, data = json.dumps(query), verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        click.echo("Failed to get alarm details " + str(response.text))
        exit()

    table = list()
    PDT = pytz.timezone('America/Los_Angeles')
    headers = ["Date & Time (PDT)", "Alarm tag" , "Active", "Viewed", "Severity", "Details" ]

    for item in items:

        temp_time = datetime.datetime.utcfromtimestamp(item["entry_time"]/1000.)
        temp_time = pytz.UTC.localize(temp_time).astimezone(PDT).strftime('%m/%d/%Y %H:%M:%S')
        clear_details = ""
        if item.get("cleared_time",""):
            temp_clr_time = datetime.datetime.utcfromtimestamp(item["cleared_time"]/1000.)
            temp_clr_time = pytz.UTC.localize(temp_clr_time).astimezone(PDT).strftime('%m/%d/%Y %H:%M:%S') + ' PDT'
            clear_details = "\nCleared By: " + str(item.get("cleared_by"," ")) + "\nCleared Time: " + str(temp_clr_time)
        elif item.get("cleared_events",""):
            clear_details = "\nOrginal alarm: " + str(item.get("cleared_events"))

        tr = [ temp_time,item['rule_name_display'], item["active"], item["acknowledged"],item["severity"],
               "UUID: " + item["uuid"] + "\nValues:\n" + json.dumps(item["values"] , sort_keys=True, indent=4)
               + clear_details ]
        table.append(tr)
        
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

@click.command()
@click.option("--uuid", help="Alarm uuid")
def alarm_details(uuid):
    """ Retrieve consumed event details for provided alarm uuid.
        \nExample command: ./alarms_apis.py alarm-details --uuid <alarm uuid value>
    """
    click.echo("\nRetrieving the consumed events for uuid %s\n"%uuid)

    url = base_url + "/alarms/uuid/%s"%uuid

    response = requests.get(url=url, headers=header, verify=False)

    headers = ["Date & Time (PDT)", "Alarm tag", "Active", "Viewed", "Consumed Events"]    
    table = list()
    PDT = pytz.timezone('America/Los_Angeles')

    if response.status_code == 200:
        items = response.json()['data']
    else:
        click.echo("Failed to get alarm details " + str(response.text))
        exit()

    for item in items:

        temp_time = datetime.datetime.utcfromtimestamp(item["entry_time"]/1000.)
        temp_time = pytz.UTC.localize(temp_time).astimezone(PDT).strftime('%m/%d/%Y %H:%M:%S')
        tr = [ temp_time, item["rule_name_display"], item["active"], item["acknowledged"], 
               json.dumps(item["consumed_events"] , sort_keys=True, indent=4) ]
        table.append(tr)

    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

@click.command()
@click.option("--uuids", help="Alarm uuid/s")
def ack_alarm(uuids):
    """ Acknowledge specific alarms of provided uuids.                  
        \nExample command: ./alarms_apis.py ack-alarm --uuid <alarm uuid value>
        \nTo ack multiple uuids seperate uuid using "," i.e. --uuid uuid-1,uuid-2
    """
    
    uuids = uuids.split(",")

    url = base_url + "/alarms/markviewed"

    payload = {
                "uuid" : uuids
              }

    response = requests.post(url=url, headers=header, data = json.dumps(payload), verify=False)
    if response.status_code == 200:
        click.echo("Acknowledged the alarms with uuid %s "%uuids)
    else:
        click.echo("Failed to ack alarms " + str(response.text))
        exit()

cli.add_command(list_alarms_tags)
cli.add_command(list_alarms)
cli.add_command(alarm_details)
cli.add_command(ack_alarm)

if __name__ == "__main__":
    cli()