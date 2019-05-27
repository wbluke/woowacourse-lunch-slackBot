import os
import slack

class LunchBot:
    def __init__(self, restaurant_repo):
        self.slack_token = os.environ['SLACK_API_TOKEN']
        self.repository = restaurant_repo

    def start(self):
        rtm_client = slack.RTMClient(token=self.slack_token)
        rtm_client.start()

    @slack.RTMClient.run_on(event='message')
    def recommend(self, **payload):
        data = payload['data']
        web_client = payload['web_client']
        rtm_client = payload['rtm_client']
        
        if '밥!' in data['text']:
            channel_id = data['channel']
            thread_ts = data['ts']
            user = data['user']

            web_client.chat_postMessage(
                channel=channel_id,
                attachments=[
                    {
                        'text': 'hi',
                    }
                ]
            )