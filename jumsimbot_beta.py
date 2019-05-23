import os
import slack
from pprint import pprint
from WorksheetReader import Worksheet, Restaurant

JSON_KEYFILE_ADDRESS = 'lunchBot-worksheet-key.json'
SHEET_NAME = 'woowacourse-lunch-sheet'

@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    pprint(payload)
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    if '밥!' in data['text']:
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        
        # web_client.chat_postMessage(channel=channel_id, text=f"Hi <@{user}>!")
        for restaurant in restaurants:
            web_client.chat_postMessage(
                channel=channel_id,
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "<" 
                            + restaurant.get_naver_place_addr() + "|" + restaurant.get_name() 
                            + "> \n 대표 메뉴 : " + restaurant.get_popular_menu() + "  가격 : " 
                            + restaurant.get_price_of_popular_menu() + " \n :thumbsup: " 
                            + restaurant.get_good() + ":thumbsdown: " + restaurant.get_bad()
                        }   
                    }
                ]
            )

worksheet = Worksheet(JSON_KEYFILE_ADDRESS, SHEET_NAME)
restaurants = []

rows = worksheet.get_all_values()
header = rows.pop(0)   

for rowNo in range(len(worksheet.get_all_restaurant_names())):
    restaurants.append(worksheet.get_restaurant(rowNo + 1))

slack_token = os.environ["SLACK_API_TOKEN"]
rtm_client = slack.RTMClient(token=slack_token)
rtm_client.start()

        