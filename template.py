
import requests, json

def quick_reps():
    q_reps = [{
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
    
    return q_reps

def movie_carousel(bronze, viewer, template):
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
                        "subtitle": template[0]['overview'],
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
                        "subtitle": template[1]['overview'],
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
                        "subtitle": template[2]['overview'],
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
                        "subtitle": template[3]['overview'],
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
                   "quick_replies": quick_reps()}
              }),
              headers={'Content-type': 'application/json'})

def music_carousel(bronze2, viewer, template):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
            params={"access_token": bronze2},
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
                        "image_url": template[0]['cover'],
                        "subtitle": template[0]['artist'],
                       },
                      {
                        "title": template[1]['title'],
                        "image_url": template[1]['cover'],
                        "subtitle": template[1]['artist'],
                      },
                      {
                        "title": template[2]['title'],
                        "image_url": template[2]['cover'],
                        "subtitle": template[2]['artist'],
                      },
                      {
                        "title": template[3]['title'],
                        "image_url": template[3]['cover'],
                        "subtitle": template[3]['artist'],
                      },
                      {
                        "title": template[4]['title'],
                        "image_url": template[4]['cover'],
                        "subtitle": template[4]['artist'],
                      },
                      {
                        "title": template[5]['title'],
                        "image_url": template[5]['cover'],
                        "subtitle": template[5]['artist'],
                      },
                      {
                        "title": template[6]['title'],
                        "image_url": template[6]['cover'],
                        "subtitle": template[6]['artist'],
                      },
                      {
                        "title": template[7]['title'],
                        "image_url": template[7]['cover'],
                        "subtitle": template[7]['artist'],
                      }
                      ]
                     }
                    },
                   "quick_replies": quick_reps()}
              }),
              headers={'Content-type': 'application/json'})
