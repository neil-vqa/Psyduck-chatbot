
from flask import Flask, request
import json, praw
import requests, random

app = Flask(__name__)
reddit = praw.Reddit(client_id='iGMNdhNR4e_Atg',
                    client_secret='xkuIbmiS2GHhNr-NkpmzPGRVYMI',
                    user_agent='web:psyduck-chatbot.herokuapp.com:v1.0 (by /u/neilthegreatest)')

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
            yield event["sender"]["id"], 'Wala ko kasabot'.encode('unicode_escape')

def post_this(gold, receiver, load):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
            params={"access_token": gold},
            data=json.dumps({
                "recipient": {"id": receiver},
                "message": {"text": load}
            }),
            headers={'Content-type': 'application/json'})
    
hi_ls = ['Hi','Hello','hi','hello','Hey']
help_ls = ['Help','help']
mixed_ls = ['Gwapo ko','Gwapa ko']
eat_ls = ['Where to eat?','Suggest food','Recommend food']
movie_ls = ['Suggest movie','Recommend movie','What to watch?']
word_list1 = ['Wat u think?','Tell me more','Speak','Hoy','Oy','Tell me']
word_list2 = ['Life tip','life tip','Tip']
word_list3 = ['Tell me a quote','Quote','Give a quote']
word_list4 = ['World news','world news','news']
            
def send_message(token, recipient, text):
    if text.decode('unicode_escape') in hi_ls:
        payload = "Psyduck? Yes I am Psyduck. Let me help you! Type Help to learn my keywords."
        post_this(token, recipient, payload)
    
    elif text.decode('unicode_escape') in help_ls:
        payload = "These are the keywords you can type so that I can interact with you well! \n Tell me a quote \n Wat u think? \n World news \n Life tip"
        post_this(token, recipient, payload)

    elif text.decode('unicode_escape') in mixed_ls:
        mixed_res = ['yuck','Yes you are...that is compared with monkeys','char']
        payload = random.choice(mixed_res)
        post_this(token, recipient, payload)
        
    elif text.decode('unicode_escape') in eat_ls:
        eat_res = ['Jollibee','Mcdo','KFC','Mang Inasal','Greenwich','Yellow Cab','S&R','Carenderia','BBQ','kwek-kwek','Bibimbap','Bulgogi','Donut','Ramen','Sushi','Lechon']
        payload = random.choice(eat_res)
        post_this(token, recipient, payload)
        
    elif text.decode('unicode_escape') in movie_ls:
        url = "https://api.themoviedb.org/3/trending/movie/day?api_key=dbc5a5e4384cceeced1c90779da712da"
        data_res = "{}"
        response = requests.request("GET", url, data=data_res)
        top_mov = json.loads(response.text)
        movlis = []
        for movie in top_mov['results']:
            title = movie['title']
            overview = '  (OVERVIEW)  ' + movie['overview']
            desc = title + overview
            movlis.append(desc)
        payload = random.choice(movlis)
        post_this(token, recipient, payload)

    elif text.decode('unicode_escape') in word_list1:
        shower = []
        for submission in reddit.subreddit('Showerthoughts+explainlikeimfive+todayilearned').hot(limit=20):
            shower.append(submission.title)
        payload = random.choice(shower)
        post_this(token, recipient, payload)
    
    elif text.decode('unicode_escape') in word_list2:
        lifer = []
        for submission in reddit.subreddit('LifeProTips').hot(limit=20):
            lifer.append(submission.title)
        payload = random.choice(lifer)
        post_this(token, recipient, payload)

    elif text.decode('unicode_escape') in word_list3:
        quoter = []
        for submission in reddit.subreddit('QuotesPorn').hot(limit=20):
            quoter.append(submission.title)
        payload = random.choice(quoter)
        post_this(token, recipient, payload)

    elif text.decode('unicode_escape') in word_list4:
        newser = []
        for submission in reddit.subreddit('worldnews').hot(limit=20):
            newt = submission.title
            newu = '  (LINK)  ' + submission.url
            newf = newt + newu
            newser.append(newf)
        payload = random.choice(newser)
        post_this(token, recipient, payload)
    
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
                
if __name__ == '__main__':
    app.run()
