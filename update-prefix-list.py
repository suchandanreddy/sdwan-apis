import requests
import sys
import json
import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler

requests.packages.urllib3.disable_warnings()

from requests.packages.urllib3.exceptions import InsecureRequestWarning

def get_logger(logfile, level):
    '''
    Create a logger
    '''
    if logfile is not None:

        '''
        Create the log directory if it doesn't exist
        '''

        fldr = os.path.dirname(logfile)
        if not os.path.exists(fldr):
            os.makedirs(fldr)

        logger = logging.getLogger()
        logger.setLevel(level)
 
        log_format = '%(asctime)s | %(levelname)-8s | %(funcName)-20s | %(lineno)-3d | %(message)s'
        formatter = logging.Formatter(log_format)
 
        file_handler = TimedRotatingFileHandler(logfile, when='midnight', backupCount=7)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        logger.addHandler(file_handler)

        return logger

    return None


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


def get_device_ids(jsessionid,token,template_id):

    if token is not None:
        headers = {'Content-Type': "application/json",'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
    else:
        headers = {'Content-Type': "application/json",'Cookie': jsessionid}

    base_url = "https://%s:%s/dataservice"%(vmanage_host,vmanage_port)

    api_url = '/template/device/config/attached/' + template_id

    url = base_url + api_url

    response = requests.get(url=url, headers=headers,verify=False)

    if response.status_code == 200:
        device_ids = []
        for device in response.json()['data']:
            device_ids.append(device['uuid'])
        if logger is not None:
            logger.info("Device ids " + str(device_ids))
        return device_ids
    else:
        if logger is not None:
            logger.error("Failed to get device ids " + str(response.text))
        exit()

def get_device_inputs(jsessionid,token,template_id, device_ids):

    if token is not None:
        headers = {'Content-Type': "application/json",'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
    else:
        headers = {'Content-Type': "application/json",'Cookie': jsessionid}

    payload = {
        'templateId': template_id,
        'deviceIds': device_ids,
        'isEdited': True,
        'isMasterEdited': False
    }

    base_url = "https://%s:%s/dataservice"%(vmanage_host,vmanage_port)

    api_url = '/template/device/config/input'

    url = base_url + api_url    

    response = requests.post(url=url, headers=headers, data=json.dumps(payload), verify=False)

    if response.status_code == 200:

        device_inputs = response.json()['data']

        for input in device_inputs:
            input['csv-templateId'] = template_id
    
        if logger is not None:
            logger.info("Device config input" + str(device_inputs))
    else:
        if logger is not None:
            logger.error("Failed to get device config input " + str(response.text))
        exit()

    return device_inputs

if __name__ == '__main__':

    try:

        log_level = logging.DEBUG
        logger = get_logger("log/data_prefix_list_logs.txt", log_level)
        vmanage_host = os.environ.get("vmanage_host")
        vmanage_port = os.environ.get("vmanage_port")
        username = os.environ.get("username")
        password = os.environ.get("password")
        prefix_list_name = os.environ.get("prefix_list_name")

        if vmanage_host is None or vmanage_port is None or username is None or password is None or prefix_list_name is None :
            print("For Windows Workstation, vManage details must be set via environment variables using below commands")
            print("set vmanage_host=198.18.1.10")
            print("set vmanage_port=443")
            print("set username=admin")
            print("set password=admin")
            print("set prefix_list_name=<date prefix list name>")
            print("For MAC OSX Workstation, vManage details must be set via environment variables using below commands")
            print("export vmanage_host=198.18.1.10")
            print("export vmanage_port=443")
            print("export username=admin")
            print("export password=admin")
            print("export prefix_list_name=<date prefix list name>")
            exit()

        entries =   [
                            {
                            "ipPrefix": "13.107.6.152/31"
                            },
                            {
                            "ipPrefix": "13.107.18.10/31"
                            },
                            {
                            "ipPrefix": "13.107.128.0/22"
                            },
                            {
                            "ipPrefix": "23.103.160.0/20"
                            },
                            {
                            "ipPrefix": "40.96.0.0/13"
                            },
                            {
                            "ipPrefix": "40.104.0.0/15"
                            },
                            {
                            "ipPrefix": "52.96.0.0/14"
                            },
                            {
                            "ipPrefix": "131.253.33.215/32"
                            },
                            {
                            "ipPrefix": "132.245.0.0/16"
                            },
                            {
                            "ipPrefix": "150.171.32.0/22"
                            },
                            {
                            "ipPrefix": "191.234.140.0/22"
                            },
                            {
                            "ipPrefix": "204.79.197.215/32"
                            },
                            {
                            "ipPrefix": "13.107.64.0/18"
                            },
                            {
                            "ipPrefix": "52.112.0.0/14"
                            },
                            {
                            "ipPrefix": "13.107.136.0/22"
                            },
                            {
                            "ipPrefix": "40.108.128.0/17"
                            },
                            {
                            "ipPrefix": "52.104.0.0/14"
                            },
                            {
                            "ipPrefix": "104.146.128.0/17"
                            },
                            {
                            "ipPrefix": "150.171.40.0/22"
                            }
                    ]


        Auth = Authentication()
        jsessionid = Auth.get_jsessionid(vmanage_host,vmanage_port,username,password)
        token = Auth.get_token(vmanage_host,vmanage_port,jsessionid)

        if token is not None:
            headers = {'Content-Type': "application/json",'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
        else:
            headers = {'Content-Type': "application/json",'Cookie': jsessionid}

        # Get Dataprefix lists

        base_url = "https://%s:%s/dataservice"%(vmanage_host,vmanage_port)

        api_url = "/template/policy/list/dataprefix"

        url = base_url + api_url

        response = requests.get(url=url, headers=headers, verify=False)

        if response.status_code == 200:
            for item in response.json()["data"] :
                if item["name"] == prefix_list_name:
                    dataprefix_listid = item["listId"]
        else:
            if logger is not None:
                logger.error("Failed to retrieve data prefix lists\n")


        inputs = []
        
        # Edit data prefix list

        payload = {
	                "name":prefix_list_name,
	                "description":"",
                    "type":"dataPrefix",
                    "listId": dataprefix_listid,
                    "entries": entries
                   }

        if logger is not None:
            logger.info("Put request payload :" + str(payload))

        api_url = '/template/policy/list/dataprefix/' + dataprefix_listid

        url = base_url + api_url

        response = requests.put(url=url, headers=headers, data=json.dumps(payload), verify=False)

        if response.status_code == 200:
            master_templates_affected = response.json()['masterTemplatesAffected']
            if logger is not None:
                logger.info("Master templates affected " + str(master_templates_affected))
        else:
            if logger is not None:
                logger.error("\nFailed to edit data prefix list " + str(response.text))
            exit()

        # Get device uuid and csv variables for each template id which is affected by prefix list edit operation

        for template_id in master_templates_affected:
            device_ids = get_device_ids(jsessionid,token,template_id)
            device_inputs = get_device_inputs(jsessionid,token,template_id,device_ids)
            inputs.append((template_id, device_inputs))


        device_template_list = []
        
        for (template_id, device_input) in inputs:
            device_template_list.append({
                'templateId': template_id,
                'isEdited': True,
                'device': device_input
            })


        #api_url for CLI template 'template/device/config/attachcli'

        api_url = '/template/device/config/attachfeature'

        url = base_url + api_url

        payload = { 'deviceTemplateList': device_template_list }

        response = requests.post(url=url, headers=headers,  data=json.dumps(payload), verify=False)

        if response.status_code == 200:
            process_id = response.json()["id"]
            if logger is not None:
                logger.info("Attach template process id " + str(response.text))
        else:
            if logger is not None:
                logger.error("Template attach process failed " + str(response.text))     

        api_url = '/device/action/status/' + process_id  

        url = base_url + api_url

        while(1):
            time.sleep(10)
            response = requests.get(url=url, headers=headers, verify=False)
            if response.status_code == 200:
                if response.json()['summary']['status'] == "done":
                    logger.info("\nTemplate push status is done")
                    print("Updated Prefix list successfully")
                    break
                else:
                    continue
            else:
                logger.error("\nFetching template push status failed " + str(response.text))
                exit()
            

    except Exception as e:
        print('Failed due to error',str(e))
            
    