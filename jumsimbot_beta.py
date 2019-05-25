import os
import slack
from pprint import pprint
from WorksheetReader import Worksheet, Restaurant

JSON_KEYFILE_ADDRESS = 'lunchBot-worksheet-key.json'
SHEET_NAME = 'woowacourse-lunch-sheet'

@slack.RTMClient.run_on(event='message')
def recommend(**payload):
    pprint(payload)
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    if '밥!' in data['text']:
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        for restaurant in restaurants:
            restaurant_color = '#000000'
            restaurant_thumb_url = 'http://cdn.wbluke.com/lunch_bot_image/'
            restaurant_type = restaurant.get_type()

            if restaurant_type == '한식':
                restaurant_color = '#218e16'
                restaurant_thumb_url += 'koreanFood.png'
            elif restaurant_type == '일식':
                restaurant_color = '#ea0000'
                restaurant_thumb_url += 'japaneseFood.png'
            elif restaurant_type == '중식':
                restaurant_color = '#401c0e'
                restaurant_thumb_url += 'chineseFood.png'
            elif restaurant_type == '양식':
                restaurant_color = '#eaff08'
                restaurant_thumb_url += 'westernFood.png'
            elif restaurant_type == '분식':
                restaurant_color = '#ff7f00'
                restaurant_thumb_url += 'flourBasedFood.png'
            elif restaurant_type == '카페':
                restaurant_color = '#fbed36'
                restaurant_thumb_url += 'cafeFood.png'
            else:
                restaurant_color = '#5ce7e3'
                restaurant_thumb_url += 'etcFood.png'

            web_client.chat_postMessage(
                channel=channel_id,
                attachments=[
                    {
                        'fallback': 'ReferenceError - ' + restaurant.get_naver_place_addr(),
                        'text': '<' + restaurant.get_naver_place_addr() + '|' + restaurant.get_name() + '>',
                        'fields': [
                            {
                                'title': '대표 메뉴',
                                'value': restaurant.get_popular_menu() + ' ' + restaurant.get_price_of_popular_menu() + '원',
                                'short': True
                            },
                            {
                                'title': '추천 정보',
                                'value': ':thumbsup: '+ restaurant.get_good() + '   :thumbsdown: ' + restaurant.get_bad(),
                                'short': True
                            }
                        ],
                        'color': restaurant_color,
			            'thumb_url': restaurant_thumb_url
                    }
                ]
            )

@slack.RTMClient.run_on(event='reaction_added')
def update_emoji(**payload):
    print('====================================== reaction_added =========================================')
    pprint(payload)
    data = payload['data']
    web_client = payload['web_client']
    channel_id = data['item']['channel']
    ts = data['item']['ts']
    user_id = data['user']

    if data['reaction'] == 'thumbsup':
        pass
        # TODO : good reaction 캐시에 업데이트
        # history API 에 ts 와 channel_id 를 사용하여 원래의 메시지에 접근
    
    elif data['reaction'] == 'thumbsdown':
        pass
        # TODO : bad reaction 캐시에 업데이트


worksheet = Worksheet(JSON_KEYFILE_ADDRESS, SHEET_NAME)
restaurants = []

rows = worksheet.get_all_values()
header = rows.pop(0)   

for rowNo in range(len(worksheet.get_all_restaurant_names())):
    restaurants.append(worksheet.get_restaurant(rowNo + 1))

slack_token = os.environ['SLACK_API_TOKEN']
rtm_client = slack.RTMClient(token=slack_token)
rtm_client.start()

        