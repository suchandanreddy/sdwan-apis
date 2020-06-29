#! /usr/bin/env python
import requests
import sys
import json
import click
import os
import tabulate
import yaml
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
    """Command line tool for monitoring Cisco SD-WAN solution components.
    """
    pass

@click.command()
def device_list():
    """ Retrieve and return network devices list.                                           
        Returns information about each device that is part of the fabric.                          
        \n Example command: ./vmanage_apis.py device-list
    """
    click.echo("\nRetrieving the devices.")

    url = base_url + "/device"

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        print("Failed to get list of devices " + str(response.text))
        exit()

    headers = ["Host-Name", "Device Type", "Device ID", "System IP", "Site ID", "Version", "Device Model"]
    table = list()

    for item in items:
        tr = [item.get('host-name'), item.get('device-type'), item.get('uuid'), item.get('system-ip'), item.get('site-id'), item.get('version'), item.get('device-model')]
        table.append(tr)
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

@click.command()
@click.option("--system_ip", help="System IP address of the device")
def system_status(system_ip):
    """ Retrieve and return information about System status of network device in SD-WAN fabric

        Example command:
            ./vmanage_apis.py system-status --system_ip 
    """

    click.secho("\nRetrieving the System Status")

    url = base_url + "/device/system/status?deviceId={0}".format(system_ip)

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        print("Failed to get system status " + str(response.text))
        exit()

    print("\nSystem status for Device:",system_ip)

    headers = ["Host name", "Up time", "Version", "Memory Used", "CPU system"]
    table = list()

    for item in items:
        tr = [item['vdevice-host-name'], item['uptime'], item['version'], item['mem_used'], item['cpu_system']]
        table.append(tr)

    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))


@click.command()
@click.option("--system_ip", help="System IP address of the device")
def interface_status(system_ip):
    """ Retrieve and return information about Interface status of network device in SD-WAN fabric

        Example command:
            ./vmanage_apis.py interface-status
    """

    click.secho("\nRetrieving the interface Status")

    url = base_url + "/device/interface/synced?deviceId={0}".format(system_ip)

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        print("Failed to get list of interface " + str(response.text))
        exit()

    print("\nInterfaces status for Device = ",system_ip)

    headers = ["Interface Name", "IP address", "VPN ID", "Operational status"]
    table = list()

    for item in items:
        if item.get('ip-address') != "-":
            tr = [item.get('ifname'), item.get('ip-address'),item.get('vpn-id'), item.get('if-oper-status')]
            table.append(tr)

    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))


@click.command()
@click.option("--system_ip", help="System IP address of the device")
def control_status(system_ip):
    """ Retrieve and return information about Control status of network device in SD-WAN fabric

        Example command:
            ./vmanage_apis.py control-status
    """

    click.secho("Retrieving the Control Status")

    url = base_url + "/device/control/synced/connections?deviceId={0}".format(system_ip)

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        click.echo("Failed to get list of devices " + str(response.text))
        exit()

    click.echo("\nControl Connection status for Device = %s"%system_ip)

    headers = ["Peer Type", "Peer System IP", "state", "Last Updated (UTC)"]
    table = list()

    for item in items:
        tr = [item['peer-type'], item['system-ip'], item['state'], time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(item['lastupdated']/1000.))]
        table.append(tr)

    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))


@click.command()
@click.option("--system_ip", help="System IP address of the device")
def device_counters(system_ip):
    """ Retrieve information about Device Counters of network device in SD-WAN fabric

        Example command:
            ./vmanage_apis.py device-counters
    """

    click.secho("Retrieving the Device Counters")

    url = base_url + "/device/counters?deviceId={0}".format(system_ip)

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        print("Failed to get device Counters " + str(response.text))
        exit()

    print("\nDevice Counters for device = ",system_ip)


    headers = ["OMP Peers Up", "OMP Peers Down", "Vsmart connections", "BFD Sessions Up", "BFD Sessions Down"]
    table = list()

    for item in items:
        try:
            tr = [item['ompPeersUp'], item['ompPeersDown'], item['number-vsmart-control-connections'], item['bfdSessionsUp'], item['bfdSessionsDown']]
            table.append(tr)
        except KeyError:
            pass

    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

@click.command()
@click.option("--template", help="Template UUID value")
def attached_devices(template):
    """Retrieve and return devices associated to a template.
        Example command:
            ./vmanage_apis.py attached-devices --template 6c7d22bc-73d5-4877-9402-26c75a22bd08
    """

    url = base_url + "/template/device/config/attached/{0}".format(template)

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        print("Failed to get template details")
        exit()

    headers = ["Host Name", "Device IP", "Site ID", "Host ID", "Host Type"]
    table = list()

    for item in items:
        tr = [item['host-name'], item['deviceIP'], item['site-id'], item['uuid'], item['personality']]
        table.append(tr)
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

@click.command()
@click.option("--target", help="ID of the device to detach")
@click.option("--sysip", help="System IP of the system to detach")
def detach(target, sysip):
    """ Detach a device template.
        Provide all template parameters and their values as arguments.
        Example command:
          ./vmanage_apis.py detach --target TargetID --sysip 1.1.1.1
    """
    click.secho("Attempting to detach template.")

    payload = {
        "deviceType":"vedge",
        "devices":[  
            {
                "deviceId":str(target),
                "deviceIP":str(sysip)
            }
        ]
    }

    url = base_url + "/template/config/device/mode/cli"

    response = requests.post(url=url, data=json.dumps(payload), headers=header, verify=False)
    if response.status_code == 200:
        id = response.json()["id"]
        url = base_url + "/device/action/status/" + str(id)
        while(1):
            status_res = requests.get(url,headers=header,verify=False)
            if status_res.status_code == 200:
                push_status = status_res.json()
                if push_status['summary']['status'] == "done":
                    if 'Success' in push_status['summary']['count']:
                        print("Changed configuration mode to CLI")
                    elif 'Failure' in push_status['summary']['count']:
                        print("Failed to change configuration mode to CLI")
                        exit()
                    break
    else:
        print("Failed to detach template with error " + response.text)
        exit()

cli.add_command(detach)
cli.add_command(device_list)
cli.add_command(system_status)
cli.add_command(interface_status)
cli.add_command(control_status)
cli.add_command(device_counters)
cli.add_command(attached_devices)

if __name__ == "__main__":
    cli()
   