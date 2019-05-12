from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/',methods=['POST'])
def alarms():
   data = json.loads(request.data)
   print(data)
   return "OK"

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001, debug=True)
