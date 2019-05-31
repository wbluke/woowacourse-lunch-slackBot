import os
from queue import Queue
from time import sleep
import datetime
from threading import Thread, Event
import logging

from domain.GspreadClient import GspreadClient
from domain.Lunchbot import LunchBot
from domain.RestaurantRepo import restaurant_repo
import domain.TimeStampTable

def upload_changed_restaurants(uploading_event):
    uploading_thread_logger = logging.getLogger("upload")
    uploading_thread_logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('upload.log')
    uploading_thread_logger.addHandler(file_handler)
    while True:
        restaurant_repo.refresh_gspread_token() # expired period : 1 hour
        uploading_thread_logger.info('Upload changed restaurants : ' + str(datetime.datetime.now()))
        restaurant_repo.upload_changed_restaurants()
        uploading_event.set()
        sleep(10)

def fetch_all_restaurants(uploading_event):
    fetching_thread_logger = logging.getLogger("fetch")
    fetching_thread_logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('fetch.log')
    fetching_thread_logger.addHandler(file_handler)
    while True:
        uploading_event.wait()
        fetching_thread_logger.info('Fetch all restaurants : ' + str(datetime.datetime.now()))
        restaurant_repo.fetch_all_restaurants()
        uploading_event.clear()

if __name__ == "__main__":
    uploading_event = Event()

    uploading_thread = Thread(target=upload_changed_restaurants, args=(uploading_event, ))
    fetch_thread = Thread(target=fetch_all_restaurants, args=(uploading_event, ))

    uploading_thread.start()
    fetch_thread.start()

    lunch_bot = LunchBot()
    lunch_bot.start()        
