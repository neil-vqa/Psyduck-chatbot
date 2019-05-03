from flask import Flask, request
import json, praw, os
import requests

app = Flask(__name__)
reddit = praw.Reddit(client_id='iGMNdhNR4e_Atg',
                    client_secret='xkuIbmiS2GHhNr-NkpmzPGRVYMI',
                    user_agent='neilthegreatest')

PAT = 'EAAfYtjnPepMBAAdaAA5we9NUZC4iELptzHwhY1ppFhBF6fYMW1UsxYmMRnllgldC04so2TNwWLdbZAOVbknoJHca1XoTwghiOFDjZB9paANUYO9Ks7GPlLPSZCwtrA30nmrVT5JWjWKX8BAlP1neorcuJkSPnszeKVNK6g3TKwZDZD'

@app.route('/', methods=['GET'])
def handle_verification():
    print ("Handling Verification.")
    if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me':
        print ("Verification successful!")
        return request.args.get('hub.challenge', '')
    else:
        print ("Verification failed!")
        return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def handle_messages():
    print ("Handling Messages")
    payload = request.get_data()
    print (payload)
    for sender, message in messaging_events(payload):
        print ("Incoming from {}: {}".format(sender, message))
        send_message(PAT, sender, message)
    return "ok"

def messaging_events(payload):
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
        elif "messsage" in event and "mid" in event["message"]:
            yield event["sender"]["id"], event["message"]["mid"].encode('unicode_escape')


def send_message(token, recipient, text):
    if "shower" in text:
        subreddit_name = "Showerthoughts"
    elif "joke" in text:
        subreddit_name = "Jokes"
    else:
        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
            params={"access_token": token},
            data=json.dumps({
                "recipient": {"id": recipient},
                "message": {"text": text.decode('unicode_escape')}
            }),
            headers={'Content-type': 'application/json'})
        if r.status_code != requests.codes.ok:
            print (r.text)
            
    if subreddit_name == "Showerthoughts":
        for submission in reddit.subreddit(subreddit_name).hot(limit=None):
            payload = submission.url
            break
            
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
            params={"access_token": token},
            data=json.dumps({
                "recipient": {"id": recipient},
                "message": {"text": payload}
            }),
            headers={'Content-type': 'application/json'})
    
    if subreddit_name == "Jokes":
        for submission in reddit.subreddit(subreddit_name).hot(limit=None):
            payload = submission.url
            break
            
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
            params={"access_token": token},
            data=json.dumps({
                "recipient": {"id": recipient},
                "message": {"text": payload}
            }),
            headers={'Content-type': 'application/json'})
           
if __name__ == '__main__':
    app.run()
