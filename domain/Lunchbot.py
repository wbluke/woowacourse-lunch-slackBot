import os
import slack
from domain.RestaurantRepo import restaurant_repo

class LunchBot:
    def __init__(self):
        self._slack_token = os.environ['SLACK_API_TOKEN']
#        self.repository = restaurant_repo

    def start(self):
        rtm_client = slack.RTMClient(token=self._slack_token)
        rtm_client.start()

    @slack.RTMClient.run_on(event='message')
    def recommend(**payload):
        data = payload['data']
        web_client = payload['web_client']
        
        if '밥!' in data['text']:
            channel_id = data['channel']
            thread_ts = data['ts']

            restaurants = restaurant_repo.get_random_recommendations_as_many_of(4)
            send_recommandation(web_client, channel_id, restaurants)

def send_recommandation(web_client, channel_id, restaurants):
    for restaurant in restaurants:            
        restaurant_type = restaurant.get_type()
        restaurant_color, restaurant_thumb_url = get_restaurant_color_and_thumb_url_by(restaurant_type)

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

def get_restaurant_color_and_thumb_url_by(restaurant_type):
    restaurant_color = '#000000'
    restaurant_thumb_url = 'http://cdn.wbluke.com/lunch_bot_image/'

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
    else:
        restaurant_color = '#5ce7e3'
        restaurant_thumb_url += 'etcFood.png'

    return restaurant_color, restaurant_thumb_url