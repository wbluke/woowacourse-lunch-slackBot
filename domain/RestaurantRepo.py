import random
import copy


class RestaurantRepo():
    def __init__(self, gspreadClient):
        self._restaurant_info = dict()
        self._changed_restaurants = set()
        self._gspreadClient = gspreadClient
        self.fetch_all_restaurants()

    def fetch_all_restaurants(self):
        all_restaurants = self._gspreadClient.get_all_restaurants()
        
        new_primary_keys = [restaurant.get_primary_key() for restaurant in all_restaurants]

        keys_to_del = []
        for primary_key in self._restaurant_info:
            if not primary_key in new_primary_keys:
                keys_to_del.append(primary_key)
        
        for key_to_del in keys_to_del:
            del self._restaurant_info[key_to_del]

        for restaurant in all_restaurants:
            self._restaurant_info[restaurant.get_primary_key()] = restaurant

    def get_random_recommendations_as_many_of(self, num_of_recommendation):
        choiced_keys = self.pick_primary_keys_by_rand(self.get_primary_keys(), num_of_recommendation)
        return [copy.deepcopy(self._restaurant_info.get(primary_key)) for primary_key in choiced_keys]

    def pick_primary_keys_by_rand(self, primary_keys, num_of_recommendation):
        print(primary_keys)
        choiced_keys = set()
        while len(choiced_keys) < num_of_recommendation:
            choiced_keys.add(random.choice(primary_keys))
        return list(choiced_keys)
    
    def get_primary_keys(self):
        return list(self._restaurant_info.keys())

    def upload_changed_restaurants(self):
        while len(self._changed_restaurants) > 0:
            primary_key = self._changed_restaurants.pop()

            good_points = self._restaurant_info[primary_key].get_good()
            bad_points = self._restaurant_info[primary_key].get_bad()
            self._gspreadClient.update_good_points_on(primary_key, good_points)
            self._gspreadClient.update_bad_points_on(primary_key, bad_points)

    def update_thumbsup(self, primary_key):
        if primary_key in self._restaurant_info:
            restaurant = self._restaurant_info[primary_key]
            restaurant.increase_good()
            self.append_primary_key_to_changed_restaurants(primary_key)

    def update_thumbsdown(self, primary_key):
        if primary_key in self._restaurant_info:
            restaurant = self._restaurant_info[primary_key]
            restaurant.increase_bad()
            self.append_primary_key_to_changed_restaurants(primary_key)

    def append_primary_key_to_changed_restaurants(self, primary_key):
        self._changed_restaurants.add(primary_key)

from domain.GspreadClient import GspreadClient

JSON_KEYFILE_ADDRESS = 'lunchBot-worksheet-key.json'
SHEET_NAME = 'woowacourse-lunch-sheet'

gspreadClient = GspreadClient(JSON_KEYFILE_ADDRESS, SHEET_NAME)
restaurant_repo = RestaurantRepo(gspreadClient)
