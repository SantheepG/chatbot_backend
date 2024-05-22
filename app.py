from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from repository import MessageRepository

load_dotenv()

app = Flask(__name__)

page_access_tkn = os.getenv('PAGE_ACCESS_TOKEN')
verify_token = os.getenv('VERIFY_TOKEN')

message_repository = MessageRepository(page_access_tkn)

@app.route('/')
def index():
    return 'Working'

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    # Verification
    if request.method == "GET":
        if request.args.get("hub.verify_token") == verify_token:
            return request.args.get("hub.challenge")
        else:
            return "Verification token mismatch", 403

    # Receives messages
    elif request.method == 'POST':
        data = request.json
        if 'entry' in data:
            for entry in data['entry']:
                for messaging_event in entry.get('messaging', []):
                    if 'message' in messaging_event:
                        sender_id = messaging_event['sender']['id']
                        message_text = messaging_event['message'].get('text')
                        if message_text:
                            message_repository.send_message(sender_id, message_text)
        else:
            print("Invalid payload structure:", data)

        return 'OK', 200

@app.route('/fb/msgs')
def fb_messages():
    data = message_repository.get_facebook_messages()
    return jsonify(data)

@app.route('/ig/msgs')
def instagram_messages():
    data = message_repository.get_instagram_messages()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
