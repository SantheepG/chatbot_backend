from flask import Flask, jsonify, request
import requests
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)


page_access_tkn = os.getenv('PAGE_ACCESS_TOKEN')
verify_token = os.getenv('VERIFY_TOKEN')

@app.route('/')
def index():
    return 'Working'

@app.route('/webhook', methods=['POST','GET'])
def webhook():
    # verification
    if request.method == "GET":
        if request.args.get("hub.verify_token") == verify_token:
            return request.args.get("hub.challenge")
        else:
            return request
    # receives msgs
    elif request.method == 'POST':
        data = request.json
        #print("Received payload:", data)  
        if 'entry' in data:
            for entry in data['entry']:
                for messaging_event in entry.get('messaging', []):
                    if 'message' in messaging_event:
                        sender_id = messaging_event['sender']['id']
                        message_text = messaging_event['message'].get('text')
                        if message_text:
                            send_message(sender_id, message_text)
        else:
            print("Invalid payload structure:", data)  

        return 'OK', 200
    
@app.route('/fb/msgs')
def fb_messages():
    external_url = 'https://graph.facebook.com/v19.0/me/conversations?fields=messages%7Bid%2Cfrom%2Cto%2Cmessage%7D&platform=messenger&'+f'access_token={page_access_tkn}'  
    response = requests.get(external_url)
    data = response.json()
    return jsonify(data)

@app.route('/ig/msgs')
def instagram_messages():
    external_url = 'https://graph.facebook.com/v19.0/me/conversations?fields=messages%7Bid%2Cfrom%2Cto%2Cmessage%7D&platform=instagram&'+f'access_token={page_access_tkn}'  
    response = requests.get(external_url)
    data = response.json()
    return jsonify(data)

 
def send_message(recipient_id, msg):
    url = 'https://graph.facebook.com/v12.0/me/messages'
    params = {'access_token': page_access_tkn}
    headers = {'Content-Type': 'application/json'}
    data = {
        'recipient': {'id': recipient_id},
        'message': {'text': msg}
    }
    response = requests.post(url, params=params, headers=headers, json=data)
    print("Response from Facebook:", response.json()) 


if __name__ == '__main__':
    app.run(debug=True)
