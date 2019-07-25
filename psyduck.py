
from flask import Flask, request
import json, praw, template, spotify_int
import requests, random, word_list

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
                "message": {"text": load,
                           "quick_replies": template.quick_reps()}
            }),
            headers={'Content-type': 'application/json'})
    
def post_pic(silver, sentto, picload):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
            params={"access_token": silver},
            data=json.dumps({
                "recipient": {"id": sentto},
                "message": {"attachment": {
                              "type": "image",
                              "payload": {
                                "url": picload
                              }},
                           "quick_replies": template.quick_reps()}
            }),
            headers={'Content-type': 'application/json'})
            
def send_message(token, recipient, text):
    if word_list.list1(text.decode('unicode_escape')) == True:
        payload = "Psyduck? Yes I am Psyduck. Let me help you! Type 'Help' to learn about my keywords."
        post_this(token, recipient, payload)
    
    elif word_list.list2(text.decode('unicode_escape')) == True:
        payload = "Keyword List: Food, Movie, Pic, Twice, Science, Random, Meme, Trivia, Quote, News, Cute"
        post_this(token, recipient, payload)
        
    elif word_list.list3(text.decode('unicode_escape')) == True:
        eater = []
        for submission in reddit.subreddit('FoodPorn').hot(limit=40):
            if (submission.link_flair_css_class == 'image') or ((submission.is_self != True) and ((".jpg" in submission.url) or (".png" in submission.url))):
                pict = {
                    "title": submission.title,
                    "p_url": submission.url
                }
                eater.append(pict)
        payloader = random.choice(eater)
        payload1 = payloader['p_url']
        post_pic(token, recipient, payload1)
        payload2 = payloader['title']
        post_this(token, recipient, payload2)
        
    elif word_list.list4(text.decode('unicode_escape')) == True:
        ##url = "https://api.themoviedb.org/3/trending/movie/day?api_key=dbc5a5e4384cceeced1c90779da712da"
        url = "https://api.themoviedb.org/3/movie/now_playing?api_key=dbc5a5e4384cceeced1c90779da712da&language=en-US&page=1"
        data_res = "{}"
        response = requests.request("GET", url, data=data_res)
        top_mov = json.loads(response.text)
        movlis = []
        for movie in top_mov['results']:
            title = movie['title']
            overview = movie['overview']
            poster = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2' + movie['poster_path']
            mov_id = str(movie['id'])
            web_view = 'https://www.themoviedb.org/movie/' + mov_id
            movdat = {
                "title": title,
                "overview": overview,
                "poster": poster,
                "movie_id": web_view
            }
            movlis.append(movdat)
        payload = random.sample(movlis, 4)
        template.movie_carousel(token, recipient, payload)

    elif word_list.list5(text.decode('unicode_escape')) == True:
        trivia = []
        for submission in reddit.subreddit('todayilearned').hot(limit=40):
            trivia.append(submission.title)
        payload = random.choice(trivia)
        post_this(token, recipient, payload)
    
    elif word_list.list14(text.decode('unicode_escape')) == True:
        shower = []
        for submission in reddit.subreddit('Showerthoughts+explainlikeimfive').hot(limit=50):
            shower.append(submission.title)
        payload = random.choice(shower)
        post_this(token, recipient, payload)
    
    elif word_list.list6(text.decode('unicode_escape')) == True:
        lifer = []
        for submission in reddit.subreddit('LifeProTips').hot(limit=30):
            lifer.append(submission.title)
        payload = random.choice(lifer)
        post_this(token, recipient, payload)

    elif word_list.list7(text.decode('unicode_escape')) == True:
        quoter = []
        for submission in reddit.subreddit('QuotesPorn').hot(limit=30):
            if (submission.link_flair_css_class == 'image') or ((submission.is_self != True) and ((".jpg" in submission.url) or (".png" in submission.url))):
                quoter.append(submission.url)
        payload = random.choice(quoter)
        post_pic(token, recipient, payload)

    elif word_list.list8(text.decode('unicode_escape')) == True:
        newser = []
        for submission in reddit.subreddit('worldnews').hot(limit=30):
            newt = submission.title
            newu = '  (Full Article)  ' + submission.url
            newf = newt + newu
            newser.append(newf)
        payload = random.choice(newser)
        post_this(token, recipient, payload)
        
    elif word_list.list9(text.decode('unicode_escape')) == True:
        awwer = []
        for submission in reddit.subreddit('aww').hot(limit=50):
            if (submission.link_flair_css_class == 'image') or ((submission.is_self != True) and ((".jpg" in submission.url) or (".png" in submission.url))):
                pict = {
                    "title": submission.title,
                    "p_url": submission.url
                }
                awwer.append(pict)
        payloader = random.choice(awwer)
        payload1 = payloader['p_url']
        post_pic(token, recipient, payload1)
        payload2 = payloader['title']
        post_this(token, recipient, payload2)

    elif word_list.list10(text.decode('unicode_escape')) == True:
        picker = []
        for submission in reddit.subreddit('pics+EarthPorn').top(time_filter='day', limit=30):
            if (submission.link_flair_css_class == 'image') or ((submission.is_self != True) and ((".jpg" in submission.url) or (".png" in submission.url))):
                pict = {
                    "title": submission.title,
                    "p_url": submission.url
                }
                picker.append(pict)
        payloader = random.choice(picker)
        payload1 = payloader['p_url']
        post_pic(token, recipient, payload1)
        payload2 = payloader['title']
        post_this(token, recipient, payload2)

    elif word_list.list11(text.decode('unicode_escape')) == True:
        once = []
        for submission in reddit.subreddit('twice').top(time_filter='day', limit=30):
            if (submission.link_flair_css_class == 'image') or ((submission.is_self != True) and ((".jpg" in submission.url) or (".png" in submission.url))):
                once.append(submission.url)
        payload = random.choice(once)
        post_pic(token, recipient, payload)
        
    elif word_list.list12(text.decode('unicode_escape')) == True:
        scientist = []
        for submission in reddit.subreddit('science').top(time_filter='week', limit=30):
            sciencet = submission.title
            scienceu = '  (Full Article)  ' + submission.url
            sciencef = sciencet + scienceu
            scientist.append(sciencef)
        payload = random.choice(scientist)
        post_this(token, recipient, payload)
        
    elif word_list.list13(text.decode('unicode_escape')) == True:
        memer = []
        for submission in reddit.subreddit('AdviceAnimals+funny').hot(limit=70):
            if (submission.link_flair_css_class == 'image') or ((submission.is_self != True) and ((".jpg" in submission.url) or (".png" in submission.url))):
                pict = {
                    "title": submission.title,
                    "p_url": submission.url
                }
                memer.append(pict)
        payloader = random.choice(memer)
        payload2 = payloader['title']
        post_this(token, recipient, payload2)
        payload1 = payloader['p_url']
        post_pic(token, recipient, payload1)
    
    elif text.decode('unicode_escape') == "Photography service":
        payload1 = "https://i.imgur.com/0LOlL2t.jpg"
        post_pic(token, recipient, payload1)
        payload2 = "Ed Montes Photography: ........."
        post_this(token, recipient, payload2)
        payload3 = "See more of our quality portraits by visiting our page: https://www.facebook.com/edmontesphoto"
        post_this(token, recipient, payload3)
    
    elif ("Music" or "music") in text.decode('unicode_escape'):
        input = text.decode('unicode_escape')
        output = input[6:]
        artist = spotify_int.get_artist(output)
        payload = spotify_int.show_recommendations_for_artist(artist)
        template.music_carousel(token, recipient, payload)
    
    else:
        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
            params={"access_token": token},
            data=json.dumps({
                "recipient": {"id": recipient},
                "message": {"text": text.decode('unicode_escape'),
                           "quick_replies": template.quick_reps()}
            }),
            headers={'Content-type': 'application/json'})
        if r.status_code != requests.codes.ok:
            print (r.text)
                
if __name__ == '__main__':
    app.run()
