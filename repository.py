import requests

class MessageRepository:
    
    def __init__(self, page_access_token):
        self.page_access_token = page_access_token

    def send_message(self, recipient_id, msg):
        url = 'https://graph.facebook.com/v12.0/me/messages'
        params = {'access_token': self.page_access_token}
        headers = {'Content-Type': 'application/json'}
        data = {
            'recipient': {'id': recipient_id},
            'message': {'text': msg}
        }
        response = requests.post(url, params=params, headers=headers, json=data)
        print("Response from Facebook:", response.json())

    def get_facebook_messages(self):
        url = f'https://graph.facebook.com/v19.0/me/conversations?fields=messages%7Bid%2Cfrom%2Cto%2Cmessage%7D&platform=messenger&access_token={self.page_access_token}'
        response = requests.get(url)
        return response.json()

    def get_instagram_messages(self):
        url = f'https://graph.facebook.com/v19.0/me/conversations?fields=messages%7Bid%2Cfrom%2Cto%2Cmessage%7D&platform=instagram&access_token={self.page_access_token}'
        response = requests.get(url)
        return response.json()
