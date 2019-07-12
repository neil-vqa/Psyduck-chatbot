
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
                "message": {"text": load,
                           "quick_replies": quick_reps}
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
                           "quick_replies": quick_reps}
            }),
            headers={'Content-type': 'application/json'})

def post_carousel(bronze, viewer, template):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
            params={"access_token": bronze},
            data=json.dumps({
              "recipient": {"id": viewer},
              "message":{
                "attachment":{
                  "type":"template",
                  "payload":{
                    "template_type":"generic",
                    "elements":[
                       {
                        "title": template[0]['title'],
                        "image_url": template[0]['poster'],
                        "buttons":[
                              {
                                "type":"web_url",
                                "url": template[0]['movie_id'],
                                "title":"Overview"
                              }
                        ]
                       },
                      {
                        "title": template[1]['title'],
                        "image_url": template[1]['poster'],
                        "buttons":[
                              {
                                "type":"web_url",
                                "url": template[1]['movie_id'],
                                "title":"Overview"
                              }
                        ]
                      },
                      {
                        "title": template[2]['title'],
                        "image_url": template[2]['poster'],
                        "buttons":[
                              {
                                "type":"web_url",
                                "url": template[2]['movie_id'],
                                "title":"Overview"
                              }
                        ]
                      },
                      {
                        "title": template[3]['title'],
                        "image_url": template[3]['poster'],
                        "buttons":[
                              {
                                "type":"web_url",
                                "url": template[3]['movie_id'],
                                "title":"Overview",
                                "webview_height_ratio": "tall"
                              }
                        ]
                      }
                      ]
                     }
                    },
                   "quick_replies": quick_reps}
              }),
              headers={'Content-type': 'application/json'})
    
hi_ls = ['Hi','Hello','hi','hello','Hey']
help_ls = ['Help','help','More keywords']
eat_ls = ['Yummy','Suggest food','Recommend food','Food']
movie_ls = ['Suggest movie','Recommend movie','What to watch?','Movie']
word_list1 = ['Wat u think?','Tell me more','Speak','Hoy','Oy','Tell me','wat u think?','Bored','Trivia']
word_list2 = ['Life tip','life tip','Tip','tip']
word_list3 = ['Tell me a quote','Quote','Give a quote','quote']
word_list4 = ['World news','world news','news','News']
word_list5 = ['Aww','Cute','Cutie','Awww','aww','cute']
word_list6 = ['Send pic','Pic pls','Pic']
word_list7 = ['TWICE','twice','Twice']
word_list8 = ['Science', 'science', 'Tell me some science']
word_list9 = ['Meme','meme','give meme','Give meme']
word_list10 = ['Shower','Random']

quick_reps = [{
    "content_type":"text",
    "title":"Trivia",
    "payload":"Trivia"
},
  {
    "content_type":"text",
    "title":"Quote",
    "payload":"Quote"
},
  {
    "content_type":"text",
    "title":"News",
    "payload":"News"
},
  {
    "content_type":"text",
    "title":"Cute",
    "payload":"Cute"
},
  {
    "content_type":"text",
    "title":"More keywords",
    "payload":"More keywords"
}
]
            
def send_message(token, recipient, text):
    if text.decode('unicode_escape') in hi_ls:
        payload = "Psyduck? Yes I am Psyduck. Let me help you! Type 'Help' to learn about my keywords."
        post_this(token, recipient, payload)
    
    elif text.decode('unicode_escape') in help_ls:
        payload = "Keyword List: Food, Movie, Pic, Twice, Science, Random, Meme"
        post_this(token, recipient, payload)
        
    elif text.decode('unicode_escape') in eat_ls:
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
        
    elif text.decode('unicode_escape') in movie_ls:
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
        post_carousel(token, recipient, payload)

    elif text.decode('unicode_escape') in word_list1:
        trivia = []
        for submission in reddit.subreddit('todayilearned').hot(limit=40):
            trivia.append(submission.title)
        payload = random.choice(trivia)
        post_this(token, recipient, payload)
    
    elif text.decode('unicode_escape') in word_list10:
        shower = []
        for submission in reddit.subreddit('Showerthoughts+explainlikeimfive').hot(limit=50):
            shower.append(submission.title)
        payload = random.choice(shower)
        post_this(token, recipient, payload)
    
    elif text.decode('unicode_escape') in word_list2:
        lifer = []
        for submission in reddit.subreddit('LifeProTips').hot(limit=30):
            lifer.append(submission.title)
        payload = random.choice(lifer)
        post_this(token, recipient, payload)

    elif text.decode('unicode_escape') in word_list3:
        quoter = []
        for submission in reddit.subreddit('QuotesPorn').hot(limit=30):
            if (submission.link_flair_css_class == 'image') or ((submission.is_self != True) and ((".jpg" in submission.url) or (".png" in submission.url))):
                quoter.append(submission.url)
        payload = random.choice(quoter)
        post_pic(token, recipient, payload)

    elif text.decode('unicode_escape') in word_list4:
        newser = []
        for submission in reddit.subreddit('worldnews').hot(limit=30):
            newt = submission.title
            newu = '  (LINK)  ' + submission.url
            newf = newt + newu
            newser.append(newf)
        payload = random.choice(newser)
        post_this(token, recipient, payload)
        
    elif text.decode('unicode_escape') in word_list5:
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

    elif text.decode('unicode_escape') in word_list6:
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

    elif text.decode('unicode_escape') in word_list7:
        once = []
        for submission in reddit.subreddit('twice').top(time_filter='day', limit=30):
            if (submission.link_flair_css_class == 'image') or ((submission.is_self != True) and ((".jpg" in submission.url) or (".png" in submission.url))):
                once.append(submission.url)
        payload = random.choice(once)
        post_pic(token, recipient, payload)
        
    elif text.decode('unicode_escape') in word_list8:
        scientist = []
        for submission in reddit.subreddit('science').top(time_filter='week', limit=30):
            sciencet = submission.title
            scienceu = '  (LINK)  ' + submission.url
            sciencef = sciencet + scienceu
            scientist.append(sciencef)
        payload = random.choice(scientist)
        post_this(token, recipient, payload)
        
    elif text.decode('unicode_escape') in word_list9:
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
