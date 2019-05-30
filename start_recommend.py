import os
from queue import Queue
from time import sleep
import datetime
from threading import Thread, Event

from domain.GspreadClient import GspreadClient
from domain.Lunchbot import LunchBot
from domain.RestaurantRepo import restaurant_repo
import domain.TimeStampTable

def upload_changed_restaurants(uploading_event):
    while True:
        print('Upload changed restaurants : ' + str(datetime.datetime.now()))
        restaurant_repo.upload_changed_restaurants()
        uploading_event.set()
        sleep(180)

def fetch_all_restaurants(uploading_event):
    while True:
        uploading_event.wait()
        print('Fetch all restaurants : ' + str(datetime.datetime.now()) + "\n")
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
