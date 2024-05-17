from flask import Flask, jsonify, request
import requests
app = Flask(__name__)

#fb page id : 291374310732336
#insta page id : 17841466466174309

page_access_tkn = "EAAGWZA4XTypwBO7UfFPeDfwnORasBptSATBlnN9ArVZCDNqCe8HOjsMeFrZCYR16FaXfDsOYsZAZAXij2xEanU6wZB38NESB2qYfD7qJeFD3RGkZANayCozAwA6KBU5smOZA1tveOhU00AuDVuzQbSIb6ZCZC26wkJPYoZA7O3T7eGxzBTaa0bJ7LIVamhZBP3TyDhd7KkgrwqYP8wZDZD"

@app.route('/')
def index():
    return 'Working'

@app.route('/webhook', methods=['POST','GET'])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == "hologo":
            return request.args.get("hub.challenge")
        else:
            return request
    elif request.method == 'POST':
        # Handle incoming messages
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
    
@app.route('/fb/messages')
def fb_messages():
    external_url = 'https://graph.facebook.com/v19.0/me/conversations?fields=messages%7Bid%2Cfrom%2Cto%2Cmessage%7D&platform=messenger&'+f'access_token={page_access_tkn}'  
    response = requests.get(external_url)
    data = response.json()
    return jsonify(data)

@app.route('/instagram/messages')
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
