import random
import copy

class RestaurantRepo():
    def __init__(self, gspreadClient):
        self._restaurant_info = dict()
        self._changed_restaurants = set()
        self._gspreadClient = gspreadClient
        self.fetch_all_restaurants()

    def refresh_gspread_token(self):
        self._gspreadClient.refresh_token()

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
        return self.get_deepcopied_restaurants_by(choiced_keys)

    def get_recommendations_as_many_of(self, num_of_recommendation, restaurant_keys):
        choiced_keys = self.pick_primary_keys_by_rand(restaurant_keys, num_of_recommendation)
        return self.get_deepcopied_restaurants_by(choiced_keys)

    def pick_primary_keys_by_rand(self, primary_keys, num_of_recommendation):
        choiced_keys = set()
        while len(choiced_keys) < num_of_recommendation:
            choiced_keys.add(random.choice(primary_keys))
        return list(choiced_keys)

    def get_deepcopied_restaurants_by(self, restaurant_keys):
        return [copy.deepcopy(self._restaurant_info.get(primary_key)) for primary_key in restaurant_keys]

    
    def get_primary_keys(self):
        return list(self._restaurant_info.keys())

    def upload_changed_restaurants(self):
        while len(self._changed_restaurants) > 0:
            primary_key = self._changed_restaurants.pop()

            good_points = self._restaurant_info[primary_key].get_good()
            bad_points = self._restaurant_info[primary_key].get_bad()
            self._gspreadClient.update_good_points_on(primary_key, good_points)
            self._gspreadClient.update_bad_points_on(primary_key, bad_points)

    def increase_thumbsup_of(self, primary_key):
        if primary_key in self._restaurant_info:
            restaurant = self._restaurant_info[primary_key]
            restaurant.increase_good()
            self.append_primary_key_to_changed_restaurants(primary_key)

    def increase_thumbsdown_of(self, primary_key):
        if primary_key in self._restaurant_info:
            restaurant = self._restaurant_info[primary_key]
            restaurant.increase_bad()
            self.append_primary_key_to_changed_restaurants(primary_key)

    def decrease_thumbsup_of(self, primary_key):
        if primary_key in self._restaurant_info:
            restaurant = self._restaurant_info[primary_key]
            restaurant.decrease_good()
            self.append_primary_key_to_changed_restaurants(primary_key)

    def decrease_thumbsdown_of(self, primary_key):
        if primary_key in self._restaurant_info:
            restaurant = self._restaurant_info[primary_key]
            restaurant.decrease_bad()
            self.append_primary_key_to_changed_restaurants(primary_key)
    
    def append_primary_key_to_changed_restaurants(self, primary_key):
        self._changed_restaurants.add(primary_key)

    def find_all_restaurants_contains(self, finding_keyword):
        all_restaurant_names = []
        for primary_key, restaurant in self._restaurant_info.items():
            all_restaurant_names.append(restaurant.get_name())
        
        return list(filter(lambda restaurant_name: finding_keyword in restaurant_name, all_restaurant_names))

    def get_restaurant_keys_by_type(self, type):
        restaurant_keys = []
        for primary_key, restaurant in self._restaurant_info.items():
            if (type == restaurant.get_type()):
                restaurant_keys.append(primary_key)
        return restaurant_keys


from domain.GspreadClient import GspreadClient

JSON_KEYFILE_ADDRESS = 'lunchBot-worksheet-key.json'
SHEET_NAME = 'woowacourse-lunch-sheet'

gspreadClient = GspreadClient(JSON_KEYFILE_ADDRESS, SHEET_NAME)
restaurant_repo = RestaurantRepo(gspreadClient)
