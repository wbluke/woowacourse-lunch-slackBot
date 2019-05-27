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
        pass

    def update_thumbsup(self, primary_key):
        pass

    def update_thumbsdown(self, primary_key):
        pass

if __name__ == "__main__":
    # for testing this class

    JSON_KEYFILE_ADDRESS = '../lunchBot-worksheet-key.json'
    SHEET_NAME = 'woowacourse-lunch-sheet'

    from domain.GspreadClient import GspreadClient

    gspreadClient = GspreadClient(JSON_KEYFILE_ADDRESS, SHEET_NAME)
    restaurantRepo = RestaurantRepo(gspreadClient)

    choiced = restaurantRepo.get_random_recommendations_as_many_of(4)
    for restaurant in choiced:
        print(type(restaurant.get_primary_key()))