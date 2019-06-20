import requests
import sys
import json
import os
import tabulate
import click
import pprint
import time
import yaml

from requests.packages.urllib3.exceptions import InsecureRequestWarning

vmanage_host = os.environ.get("vmanage_host")
vmanage_port = os.environ.get("vmanage_port")
username = os.environ.get("username")
password = os.environ.get("password")


if vmanage_host is None or vmanage_port is None or username is None or password is None:
    print("For Windows Workstation, vManage details must be set via environment variables using below commands")
    print("set vmanage_host=198.18.1.10")
    print("set vmanage_port=443")
    print("set username=admin")
    print("set password=admin")
    print("For MAC OSX Workstation, vManage details must be set via environment variables using below commands")
    print("export vmanage_host=198.18.1.10")
    print("export vmanage_port=443")
    print("export username=admin")
    print("export password=admin")
    exit()

requests.packages.urllib3.disable_warnings()

class rest_api_lib:
    def __init__(self, vmanage_host,vmanage_port, username, password):
        self.vmanage_host = vmanage_host
        self.vmanage_port = vmanage_port
        self.session = {}
        self.login(self.vmanage_host, username, password)

    def login(self, vmanage_host, username, password):
        
        """Login to vmanage"""

        base_url = 'https://%s:%s/'%(self.vmanage_host, self.vmanage_port)

        login_action = '/j_security_check'

        #Format data for loginForm
        login_data = {'j_username' : username, 'j_password' : password}

        #Url for posting login data
        login_url = base_url + login_action
        url = base_url + login_url

        sess = requests.session()

        #If the vmanage has a certificate signed by a trusted authority change verify to True

        login_response = sess.post(url=login_url, data=login_data, verify=False)

    
        if b'<html>' in login_response.content:
            print ("Login Failed")
            sys.exit(0)

        self.session[vmanage_host] = sess

    def get_request(self, mount_point):
        """GET request"""
        url = "https://%s:%s/dataservice/%s"%(self.vmanage_host, self.vmanage_port, mount_point)
        print(url)
      
        response = self.session[self.vmanage_host].get(url, verify=False)
        
        return response

    def post_request(self, mount_point, payload, headers={'Content-type': 'application/json', 'Accept': 'application/json'}):
        """POST request"""
        url = "https://%s:%s/dataservice/%s"%(self.vmanage_host, self.vmanage_port, mount_point)
        #print(url)
        payload = json.dumps(payload)
        #print (payload)

        response = self.session[self.vmanage_host].post(url=url, data=payload, headers=headers, verify=False)
        #print(response.text)
        #exit()
        #data = response
        return response


#Create session with vmanage 

vmanage_session = rest_api_lib(vmanage_host, vmanage_port, username, password)

@click.group()
def cli():
    """Command line tool for deploying templates to CISCO SDWAN.
    """
    pass

@click.command()
def list_devices():

    """ Retrieve and return information about network devices in SD-WAN fabric.

        Example command:
            ./vmanage_apis.py list_devices
    """
    click.secho("Retrieving the device list")

    response = vmanage_session.get_request('device').json()

    items = response['data']

    print("\nDevice details retrieved for one network device") 
       
    pprint.pprint(items[5])

    print("\nlist of all devices retrieved")

    headers = ["Host-Name", "Device Type", "Latitude", "Longitude", "Certificate\nValidity", "Version", "Device Model", "System IP"]
    table = list()

    for item in items:
        tr = [item['host-name'], item['device-type'], item['latitude'], item['longitude'], item['certificate-validity'], item['version'], item['device-model'], item['system-ip']]
        table.append(tr)
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

@click.command()
@click.option("--system_ip", help="System IP address of the device")
def system_status(system_ip):
    """ Retrieve and return information about system status of network device in SD-WAN fabric

        Example command:
            ./vmanage_apis.py system_status
    """

    click.secho("Retrieving the System Status")

    url = "device/system/status?deviceId={0}".format(system_ip)

    response = vmanage_session.get_request(url).json()

    items = response['data']

    print("\nSystem status for Device = ",system_ip)

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
            ./vmanage_apis.py interface_status
    """

    click.secho("Retrieving the interface Status")

    url = "device/interface/synced?deviceId={0}".format(system_ip)

    response = vmanage_session.get_request(url).json()

    items = response['data']

    print("\nInterfaces status for Device = ",system_ip)

    headers = ["Interface Name", "Operational status"]
    table = list()

    for item in items:
        tr = [item['ifname'], item['if-oper-status']]
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
            ./vmanage_apis.py interface_status
    """

    click.secho("Retrieving the Control Status")

    url = "device/control/synced/connections?deviceId={0}".format(system_ip)

    response = vmanage_session.get_request(url).json()

    items = response['data']

    print("\nControl Connection status for Device = ",system_ip)

    headers = ["Peer Type", "Peer System IP", "state", "Last Updated"]
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
    """ Retrieve and return information about Device Counters of network device in SD-WAN fabric

        Example command:
            ./vmanage_apis.py interface_status
    """

    click.secho("Retrieving the Device Counters")

    url = "device/counters?deviceId={0}".format(system_ip)

    response = vmanage_session.get_request(url).json()

    items = response['data']

    print("\nDevice Counters for Device = ",system_ip)


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
def template_list():
    """Retrieve and return templates list.
        Returns the templates available on the vManage instance.
        Example command:
            ./sdwan.py template_list
    """
    click.secho("Retrieving the templates available.")

    response = vmanage_session.get_request('template/device').json()

    items = response['data']

    headers = ["Template Name", "Device Type", "Template ID", "Attached devices", "Template version"]
    table = list()

    for item in items:
        tr = [item['templateName'], item['deviceType'], item['templateId'], item['devicesAttached'], item['templateAttached']]
        table.append(tr)
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))


@click.command()
@click.option("--input_yaml", help="ID of the  to detach")
def create_feature_template(input_yaml):
    """create template with Cisco SDWAN.
        Provide all template parameters and their values as arguments.
        Example command:
          ./vmanage_apis.py create-template --input_yaml=banner.yaml
    """
    click.secho("Creating feature template based on yaml file details")

    print("Loading Network Configuration Details from YAML File")
    with open(input_yaml) as f:
        config = yaml.safe_load(f.read())

    #payload = {"templateName":"vedge_cloud_lab","templateMinVersion":"15.0.0","templateDescription":"vedge_cloud_test","templateType":"banner","templateDefinition":{"login":{"vipObjectType":"object","vipType":"constant","vipValue":"test_banner","vipVariableName":"banner_login"},"motd":{"vipObjectType":"object","vipType":"constant","vipValue":"test_banner","vipVariableName":"banner_motd"}},"deviceType":["vedge-cloud"],"deviceModels":[{"name":"vedge-cloud","displayName":"vEdge Cloud","deviceType":"vedge","isCliSupported":True,"isCiscoDeviceModel":False}],"factoryDefault":False}

    payload = {
    "templateName": config["template_name"],
    "templateMinVersion": "15.0.0",
    "templateDescription": config["template_description"],
    "templateType": "banner",
    "templateDefinition": {
        "login": {
            "vipObjectType": "object",
            "vipType": "constant",
            "vipValue": config["login_banner"],  # using the values defined for login banner in yaml file
            "vipVariableName": "banner_login"
        },
        "motd": {
            "vipObjectType": "object",
            "vipType": "constant",
            "vipValue": config["motd_banner"],  # using the values defined for motd banner in yaml file
            "vipVariableName": "banner_motd"
        }
    },
    "deviceType": [
        config["device_type"]
    ],
    "deviceModels": [
        {
            "name": "vedge-cloud",
            "displayName": "vEdge Cloud",
            "deviceType": "vedge",
            "isCliSupported": True,
            "isCiscoDeviceModel": False
        }
    ],
    "factoryDefault": False
    }


    response = vmanage_session.post_request('template/feature/', payload)
    if response.status_code == 200:
        print("\nCreated banner template ID: ", response.json())
    else:
        print("\nFailed creating banner template, error: ",response.text)


@click.command()
def factory_templates_list():
    """Retrieve and return factory default feature templates list.
        Returns the templates available on the vManage instance.
        Example command:
            ./sdwan.py template_list
    """
    click.secho("Retrieving the templates available.")

    response = vmanage_session.get_request('template/feature').json()

    items = response['data']

    headers = ["Template Name", "Template Type", "Template ID"]
    table = list()

    for item in items:
        if item['factoryDefault']:
            tr = [item['templateName'], item['templateType'], item['templateId']]
            table.append(tr)
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))


cli.add_command(list_devices)
cli.add_command(template_list)
cli.add_command(system_status)
cli.add_command(interface_status)
cli.add_command(control_status)
cli.add_command(device_counters)
cli.add_command(create_feature_template)
cli.add_command(factory_templates_list)

if __name__ == "__main__":
    cli()

