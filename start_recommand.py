import os
from queue import Queue
from time import sleep
from threading import Thread

import domain.GspreadClient
import domain.Lunchbot
from domain.RestaurantRepo import RestaurantRepo
import domain.TimeStampTable

JSON_KEYFILE_ADDRESS = 'lunchBot-worksheet-key.json'
SHEET_NAME = 'woowacourse-lunch-sheet'
slack_token = os.environ['SLACK_API_TOKEN']

restaurant_repo = RestaurantRepo()

def run_lunchbot():
    while True:
        print("start lunchbot")
        sleep(1.5)

def upload_changed_restaurants():
    while True:
        print("start gspread client")
        sleep(60)

def fetch_all_restaurants():
    pass

if __name__ == "__main__":

    uploading_thread = Thread(target=upload_changed_restaurants)
    lunchbot_thread = Thread(target=run_lunchbot)
    fetch_thread = Thread(target=fetch_all_restaurants)

    lunchbot_thread.start()
    uploading_thread.start()

    lunchbot_thread.join()
    print("?")