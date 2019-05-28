import os
from queue import Queue
from time import sleep
from threading import Thread

from domain.GspreadClient import GspreadClient
from domain.Lunchbot import LunchBot
from domain.RestaurantRepo import restaurant_repo
import domain.TimeStampTable

# JSON_KEYFILE_ADDRESS = 'lunchBot-worksheet-key.json'
# SHEET_NAME = 'woowacourse-lunch-sheet'
# gspreadClient = GspreadClient(JSON_KEYFILE_ADDRESS, SHEET_NAME)

# restaurant_repo = RestaurantRepo(gspreadClient)

def upload_changed_restaurants():
    print("start gspread client")

def fetch_all_restaurants():
    
    pass

if __name__ == "__main__":
    uploading_thread = Thread(target=upload_changed_restaurants)
    fetch_thread = Thread(target=fetch_all_restaurants)

    lunch_bot = LunchBot()
    lunch_bot.start()        
    
    uploading_thread.start()
    fetch_thread.start()

    uploading_thread.join()
    fetch_thread.join()