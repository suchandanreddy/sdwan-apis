# sdwan-apis

### Requirements

To use this application you will need:

* Python 3.7+
* Cisco SD-WAN 18.3+

### Install and Setup

Clone the code to local machine.

```
git clone https://github.com/suchandanreddy/sdwan-apis.git
cd sdwan-apis
```

Setup Python Virtual Environment (requires Python 3.7+)

```
python3.7 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Setup local environment variables to provide vManage instance details.

Examples:

```
export vmanage_host=sdwandemo.cisco.com
export vmanage_port=8443
export username=demo
export password=demo
```
