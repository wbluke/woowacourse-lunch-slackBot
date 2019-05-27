import os
from queue import Queue
from time import sleep
from threading import Thread

from domain.GspreadClient import GspreadClient
from domain.Lunchbot import LunchBot
from domain.RestaurantRepo import RestaurantRepo
import domain.TimeStampTable

JSON_KEYFILE_ADDRESS = 'lunchBot-worksheet-key.json'
SHEET_NAME = 'woowacourse-lunch-sheet'
gspreadClient = GspreadClient(JSON_KEYFILE_ADDRESS, SHEET_NAME)

restaurant_repo = RestaurantRepo(gspreadClient)

def run_lunchbot():
    lunch_bot = LunchBot(restaurant_repo)
    lunch_bot.start()        

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
    fetch_thread.start()

    lunchbot_thread.join()