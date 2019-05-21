import os
import slack
from pprint import pprint

@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    pprint(payload)
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    if '점심!' in data['text']:
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']
        
        # web_client.chat_postMessage(channel=channel_id, text=f"Hi <@{user}>!")
        web_client.chat_postMessage(
            channel=channel_id,\
            blocks=[\
                {\
                    "type": "section",\
                    "text": {\
                        "type": "mrkdwn",\
                        "text": "Danny Torrence left the following review for your property:"\
                    }   \
                },\
                {\
                    "type": "section",\
                    "text": {\
                        "type": "mrkdwn",\
                        "text": "<https://store.naver.com/restaurants/detail?id=1390661394|Overlook Hotel> \n :star: \n Doors had too many axe holes, guest in room " +\
                        "237 was far too rowdy, whole place felt stuck in the 1920s."\
                    },\
                    "accessory": {\
                        "type": "image",\
                        "image_url": "https://images.pexels.com/photos/750319/pexels-photo-750319.jpeg",\
                        "alt_text": "Haunted hotel image"\
                    }\
                },\
                {\
                    "type": "section",\
                    "fields": [\
                        {\
                            "type": "mrkdwn",\
                            "text": "*Average Rating*\n1.0"\
                        }\
                    ]\
                }\
            ]\
        )

slack_token = os.environ["SLACK_API_TOKEN"]
rtm_client = slack.RTMClient(token=slack_token)
rtm_client.start()
