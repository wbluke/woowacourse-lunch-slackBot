import os
from queue import Queue
from time import sleep
import datetime
from pytz import timezone, utc
from threading import Thread, Event
import logging
import asyncio

from domain.GspreadClient import GspreadClient
from domain.Lunchbot import LunchBot
from domain.RestaurantRepo import restaurant_repo
import domain.TimeStampTable

KST = timezone('Asia/Seoul')

def upload_changed_restaurants(uploading_event):
    uploading_thread_logger = logging.getLogger("upload")
    uploading_thread_logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('lunchbot.log')
    uploading_thread_logger.addHandler(file_handler)
    while True:
        restaurant_repo.refresh_gspread_token() # expired period : 1 hour
        now = datetime.datetime.utcnow()
        uploading_thread_logger.info('Upload changed restaurants : ' + str(utc.localize(now).astimezone(KST)))
        try:
            restaurant_repo.upload_changed_restaurants()
        except Exception as e:
            uploading_thread_logger.exception(e)
        uploading_event.set()
        sleep(180)

def fetch_all_restaurants(uploading_event):
    fetching_thread_logger = logging.getLogger("fetch")
    fetching_thread_logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('lunchbot.log')
    fetching_thread_logger.addHandler(file_handler)
    while True:
        uploading_event.wait()
        now = datetime.datetime.utcnow()
        fetching_thread_logger.info('Fetch all restaurants : ' + str(utc.localize(now).astimezone(KST)))
        try:
            restaurant_repo.fetch_all_restaurants()
        except Exception as e:
            fetching_thread_logger.exception(e)
        uploading_event.clear()

if __name__ == "__main__":
    uploading_event = Event()

    uploading_thread = Thread(target=upload_changed_restaurants, args=(uploading_event, ))
    fetch_thread = Thread(target=fetch_all_restaurants, args=(uploading_event, ))

    uploading_thread.start()
    fetch_thread.start()

    lunch_bot = LunchBot()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(lunch_bot.start(loop))
