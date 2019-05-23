from flask import Flask, request, jsonify
from ciscosparkapi import CiscoSparkAPI, SparkApiError
import json
import os
import slack

bearer_token = os.environ.get("bearer_token")
room_id = os.environ.get("room_id")
slack_token = os.environ.get('slack_api_token')
slack_channel = os.environ.get('slack_channel')

if bearer_token is None or room_id is None or slack_token is None:
    print("\nWebex Teams Authorization and roomId , Slack Token and Channel name details must be set via environment variables using below commands")
    print("export bearer_token=<authorization bearer token>")
    print("export room_id=<webex teams room-id>")
    print("export slack_token=<slack token>")
    print("export slack_channel=<slack channel name>")
    exit()

app = Flask(__name__)

@app.route('/',methods=['POST'])
def alarms():
   try:
      data = json.loads(request.data)
      print(data)
      message =  "Team, alarm event : **" + data['eventname'] + "** ------ **" + data['message'] + "** is recieved from vManage and here are the complete details <br><br>"  + str(data)
      slack_message = "Team, alarm event : *" + data['eventname'] + "* ------ *" + data['message'] + "* is recieved from vManage and here are the complete details \n\n"  + str(data)
      api = CiscoSparkAPI(access_token=bearer_token)
      res=api.messages.create(roomId=room_id, markdown=message)
      client = slack.WebClient(token=slack_token)
      response = client.chat_postMessage(channel='#webhook', text=slack_message, mrkdwn=True)
      assert response["ok"]
      #assert response["message"]["text"] == "Hello world!"
      print(res)
   except Exception as exc:
      return jsonify(str(exc)), 500
   
   return jsonify("Message sent to Webex Teams and Slack"), 200

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001, debug=True)
