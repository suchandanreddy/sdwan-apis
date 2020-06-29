from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
import json
import datetime
import pytz
import tabulate

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'sevt'
app.config['BASIC_AUTH_PASSWORD'] = 'sevt'

basic_auth = BasicAuth(app)

@app.route('/',methods=['POST'])
@basic_auth.required
def alarms():
   try:
      data = json.loads(request.data)
      PDT = pytz.timezone('America/Los_Angeles')
            
      temp_time = datetime.datetime.utcfromtimestamp(data['entry_time']/1000.)
      temp_time = pytz.UTC.localize(temp_time).astimezone(PDT).strftime('%m/%d/%Y %H:%M:%S') + ' PDT'

      table = list()
      headers = ["Date & Time (PDT)", "Alarm Name" , "Severity", "Details" ]

      tr = [ temp_time, data['rule_name_display'] , data['severity'], 
             "UUID: " + data["uuid"] + "\nValues:\n" + json.dumps(data["values"] , sort_keys=True, indent=4) ]
      
      table.append(tr)
        
      try:
          print(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
      except UnicodeEncodeError:
          print(tabulate.tabulate(table, headers, tablefmt="grid"))
      
   except Exception as exc:
      print(exc)
      return jsonify(str(exc)), 500
   
   return jsonify("Parsed Webhook Notification Successfully"), 200

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001, debug=True)