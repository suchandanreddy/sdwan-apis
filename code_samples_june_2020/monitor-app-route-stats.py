#! /usr/bin/env python

import requests
import sys
import json
import os
import time
import tabulate
import yaml
import click
import pytz
import datetime
import pandas as pd
from pandas import ExcelWriter
import cmd

requests.packages.urllib3.disable_warnings()

from requests.packages.urllib3.exceptions import InsecureRequestWarning


vmanage_host = os.environ.get("vmanage_host")
vmanage_port = os.environ.get("vmanage_port")
vmanage_username = os.environ.get("vmanage_username")
vmanage_password = os.environ.get("vmanage_password")

if vmanage_host is None or vmanage_port is None or vmanage_username is None or vmanage_password is None:
    print("For Windows Workstation, vManage details must be set via environment variables using below commands")
    print("set vmanage_host=198.18.1.10")
    print("set vmanage_port=8443")
    print("set vmanage_username=admin")
    print("set vmanage_password=admin")
    print("For MAC OSX Workstation, vManage details must be set via environment variables using below commands")
    print("export vmanage_host=198.18.1.10")
    print("export vmanage_port=8443")
    print("export vmanage_username=admin")
    print("export vmanage_password=admin")
    exit()


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
            if logger is not None:
                logger.error("No valid JSESSION ID returned\n")
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
    """Command line tool for monitoring Application Aware Routing Statistics(Latency/Loss/Jitter/vQoE Score).
    """
    pass

@click.command()
def approute_fields():
    """ Retrieve App route Aggregation API Query fields.                                  
        \nExample command: ./monitor-app-route-stats.py approute-fields
    """

    try:
        api_url = "/statistics/approute/fields"

        url = base_url + api_url

        response = requests.get(url=url, headers=header, verify=False)

        if response.status_code == 200:
            items = response.json()
        else:
            click.echo("Failed to get list of App route Query fields " + str(response.text))
            exit()

        tags = list()
        cli = cmd.Cmd()

        for item in items:
            tags.append(item['property'] + "(" + item['dataType'] + ")" )

        click.echo(cli.columnize(tags,displaywidth=120))

    except Exception as e:
        print('Exception line number: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

@click.command()
def approute_stats():
    """ Create Average Approute statistics for all tunnels between provided 2 routers for last 1 hour.                                  
        \nExample command: ./monitor-app-route-stats.py approute-stats
    """

    try:

        rtr1_systemip = input("Enter Router-1 System IP address : ")
        rtr2_systemip = input("Enter Router-2 System IP address : ")

        # Get app route statistics for tunnels between router-1 and router-2

        api_url = "/statistics/approute/fec/aggregation"

        payload = {
                    "query": {
                        "condition": "AND",
                        "rules": [
                                    {
                                        "value": [
                                        "1"
                                        ],
                                        "field": "entry_time",
                                        "type": "date",
                                        "operator": "last_n_hours"
                                    },
                                    {
                                        "value": [
                                        rtr1_systemip
                                        ],
                                        "field": "local_system_ip",
                                        "type": "string",
                                        "operator": "in"
                                    },
                                    {
                                        "value": [
                                        rtr2_systemip
                                        ],
                                        "field": "remote_system_ip",
                                        "type": "string",
                                        "operator": "in"
                                    }
                                ]
                    },
                    "aggregation": {
                        "field": [
                                    {
                                        "property": "name",
                                        "sequence": 1,
                                        "size": 6000
                                    }
                                ],
                        "metrics": [
                                    {
                                        "property": "loss_percentage",
                                        "type": "avg"
                                    },
                                    {
                                        "property": "vqoe_score",
                                        "type": "avg"
                                    },
                                    {
                                        "property": "latency",
                                        "type": "avg"
                                    },
                                    {
                                        "property": "jitter",
                                        "type": "avg"
                                    }
                                ]
                                    }
                    }

        url = base_url + api_url

        response = requests.post(url=url, headers=header, data=json.dumps(payload), verify=False)

        if response.status_code == 200:
            app_route_stats = response.json()["data"]
            app_route_stats_headers = ["Tunnel name", "vQoE score", "Latency", "Loss percentage", "Jitter"]
            table = list()

            click.echo("\nAverage App route statistics between %s and %s for last 1 hour\n"%(rtr1_systemip,rtr2_systemip))
            for item in app_route_stats:
                tr = [item['name'], item['vqoe_score'], item['latency'], item['loss_percentage'], item['jitter']]
                table.append(tr)
            try:
                click.echo(tabulate.tabulate(table, app_route_stats_headers, tablefmt="fancy_grid"))
            except UnicodeEncodeError:
                click.echo(tabulate.tabulate(table, app_route_stats_headers, tablefmt="grid"))
            
        else:
            click.echo("Failed to retrieve app route statistics\n")

        payload = {
                    "query": {
                        "condition": "AND",
                        "rules": [
                        {
                            "value": [
                            "1"
                            ],
                            "field": "entry_time",
                            "type": "date",
                            "operator": "last_n_hours"
                        },
                        {
                            "value": [
                            rtr2_systemip
                            ],
                            "field": "local_system_ip",
                            "type": "string",
                            "operator": "in"
                        },
                        {
                            "value": [
                            rtr1_systemip
                            ],
                            "field": "remote_system_ip",
                            "type": "string",
                            "operator": "in"
                        }
                        ]
                    },
                    "aggregation": {
                        "field": [
                        {
                            "property": "name",
                            "sequence": 1,
                            "size": 6000
                        }
                        ],
                        "metrics": [
                        {
                            "property": "loss_percentage",
                            "type": "avg"
                        },
                        {
                            "property": "vqoe_score",
                            "type": "avg"
                        },
                        {
                            "property": "latency",
                            "type": "avg"
                        },
                        {
                            "property": "jitter",
                            "type": "avg"
                        }
                        ]
                    }
                    }

        response = requests.post(url=url, headers=header, data=json.dumps(payload), verify=False)

        if response.status_code == 200:
            app_route_stats = response.json()["data"]
            app_route_stats_headers = ["Tunnel name", "vQoE score", "Latency", "Loss percentage", "Jitter"]
            table = list()

            click.echo("\nAverage App route statistics between %s and %s for last 1 hour\n"%(rtr2_systemip,rtr1_systemip))
            for item in app_route_stats:
                tr = [item['name'], item['vqoe_score'], item['latency'], item['loss_percentage'], item['jitter']]
                table.append(tr)
            try:
                click.echo(tabulate.tabulate(table, app_route_stats_headers, tablefmt="fancy_grid"))
            except UnicodeEncodeError:
                click.echo(tabulate.tabulate(table, app_route_stats_headers, tablefmt="grid"))
            
        else:
            click.echo("Failed to retrieve app route statistics\n")


    except Exception as e:
        print('Exception line number: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            

@click.command()
@click.option("--hub_list_file", help="YAML file with list of hub system ip addresses")
def approute_report(hub_list_file):
    """ \nCreate Average Approute statistics report.                                      
        \nProvide YAML file which includes list of Hub System IP addresses.                           
        \nExample command: ./monitor-app-route-stats.py approute-report --hub_list_file <.yaml>
    """

    try:
        try: 
            start_date = input("Please enter start date(YYYY-MM-DD): ")
            time.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect start data format, please enter in YYYY-MM-DD") 
        try:    
            end_date = input("Please enter end date(YYYY-MM-DD): ")
            time.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect end data format, please enter in YYYY-MM-DD")         

        with open(hub_list_file) as f:
            config = yaml.safe_load(f.read())

        # Get Device Inventory details 

        api_url = "/device"

        url = base_url + api_url

        response = requests.get(url=url, headers=header, verify=False)

        device_inv = dict()

        if response.status_code == 200:
            temp = response.json()["data"]
            for item in temp:
                if item["personality"] == "vedge":
                    device_inv[item["system-ip"]] = [{'hostname' : item["host-name"]} , {'siteid' : item["site-id"]}]
        else:
            click.echo("Failed to retrieve device inventory\n")

        # Get app route statistics for tunnels between Hub routers and Spoke routers.

        # open excel file 
        writer = ExcelWriter('Tunnel Statistics %s to %s.xlsx'%(start_date,end_date))

        PDT = pytz.timezone('America/Los_Angeles')
        file_name   = open("Tunnel Statistics %s to %s.csv"%(start_date,end_date),"w")
        csv_content = ""

        for hub in config["hub_routers"]:

            api_url = "/statistics/approute/fec/aggregation"

            payload = {
                            "query": {
                                "condition": "AND",
                                "rules": [
                                {
                                    "value": [
                                              start_date+"T00:00:00 UTC",
                                              end_date+"T23:59:59 UTC" 
                                             ],
                                    "field": "entry_time",
                                    "type": "date",
                                    "operator": "between"
                                },
                                {
                                    "value": [
                                            hub["system_ip"]
                                            ],
                                    "field": "local_system_ip",
                                    "type": "string",
                                    "operator": "in"
                                }
                                ]
                            },
                            "aggregation": {
                                "field": [
                                {
                                    "property": "name",
                                    "sequence": 1,
                                    "size": 6000
                                },
                                {
                                    "property": "proto",
                                    "sequence": 2
                                },
                                {
                                    "property": "local_system_ip",
                                    "sequence": 3
                                },
                                {
                                    "property": "remote_system_ip",
                                    "sequence": 4
                                }
                                ],
                                "histogram": {
                                                "property": "entry_time",
                                                "type": "hour",
                                                "interval": 24,
                                                "order": "asc"
                                             },
                                "metrics": [
                                {
                                    "property": "latency",
                                    "type": "avg"
                                },
                                {
                                    "property": "jitter",
                                    "type": "avg"
                                },
                                {
                                    "property": "loss_percentage",
                                    "type": "avg"
                                },
                                {
                                    "property": "vqoe_score",
                                    "type": "avg"
                                }
                                ]
                            }
                            }

            url = base_url + api_url

            response = requests.post(url=url, headers=header, data=json.dumps(payload), verify=False)
            if response.status_code == 200:
                app_route_stats = response.json()["data"]
                app_route_stats_headers = ["Date (PDT)", "Hub", "Hub Siteid", "Spoke", "Spoke Siteid", "Tunnel name", "vQoE score", "Latency", "Loss percentage", "Jitter"]
                date_list = list()
                hub_list = list()
                hub_siteid_list = list()
                spoke_list = list()
                spoke_siteid_list = list()
                tunnel_name_list = list()
                vqoe_list = list()
                latency_list = list()
                loss_list = list()
                jitter_list = list()
                table = list()


                for item in app_route_stats:

                    temp_time = datetime.datetime.utcfromtimestamp(item['entry_time']/1000.)
                    temp_time = pytz.UTC.localize(temp_time).astimezone(PDT).strftime('%m/%d/%Y')
                    #date_list.append(time.strftime('%m/%d/%Y',  time.gmtime(item['entry_time']/1000.)))

                    tr = [temp_time, device_inv[item['local_system_ip']][0]['hostname'], device_inv[item['local_system_ip']][1]['siteid'], device_inv[item['remote_system_ip']][0]['hostname'], device_inv[item['remote_system_ip']][1]['siteid'], item['name'], item['vqoe_score'], item['latency'], item['loss_percentage'], item['jitter']]
                    table.append(tr)

                    date_list.append(temp_time)
                    hub_list.append(device_inv[item['local_system_ip']][0]['hostname'])
                    hub_siteid_list.append(device_inv[item['local_system_ip']][1]['siteid'])
                    spoke_list.append(device_inv[item['remote_system_ip']][0]['hostname'])
                    spoke_siteid_list.append(device_inv[item['remote_system_ip']][1]['siteid'])
                    tunnel_name_list.append(item['name'])
                    vqoe_list.append(item['vqoe_score'])
                    latency_list.append(item['latency'])
                    loss_list.append(item['loss_percentage'])
                    jitter_list.append(item['jitter'])
                
                csv_content = csv_content + tabulate.tabulate(table, app_route_stats_headers, tablefmt="csv") + "\n"
                excel_content = dict()
                excel_content["Date (PDT)"] = date_list
                excel_content["Hub"] = hub_list
                excel_content["Hub Siteid"] = hub_siteid_list
                excel_content["Spoke"] = spoke_list
                excel_content["Spoke Siteid"] = spoke_siteid_list
                excel_content["Tunnel name"] = tunnel_name_list
                excel_content["vQoE score"] = vqoe_list
                excel_content["Latency"] = latency_list
                excel_content["Loss percentage"] = loss_list
                excel_content["Jitter"] = jitter_list

                df = pd.DataFrame(excel_content)
                df.to_excel(writer, device_inv[hub["system_ip"]][0]['hostname'] ,index=False)
                    
            else:
                click.echo("Failed to retrieve app route statistics\n")

        writer.save()
        file_name.write(csv_content)
        file_name.close()
        click.echo("\nCreated report of Average App Route statistics for Tunnels between Hub routers and Spokes for %s and %s\n"%(start_date,end_date))


    except Exception as e:
        print('Exception line number: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

cli.add_command(approute_fields)
cli.add_command(approute_stats)
cli.add_command(approute_report)

if __name__ == "__main__":
    cli()