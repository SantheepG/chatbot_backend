from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return 'Working'

@app.route('/instagram/messages')
def instagram_messages():
    external_url = 'https://graph.facebook.com/v19.0/me/conversations?fields=messages{message}&access_token=EAAGWZA4XTypwBO2DpU3wqg2WZBRRzYQSGodgMWcMGK0OerETTKD0ZBTI9T8StLOj8OgDHm1iWnxIgwfZCmqlV5m9LZCZBIQV0O0XBs6H2GKmiYf0W2ADVBK4GXmpmsp7lmTxOTJy9U9sU9yETl6VvfQE9by2tF2BRGb9YAFQSBBX1ojS2fZBFiPmgZBe3b59hz1SGyoX8WZBfiwHwa5w3wTBfFrlXSfqu1KJswQZDZD'  
    response = requests.get(external_url)
    data = response.json()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
