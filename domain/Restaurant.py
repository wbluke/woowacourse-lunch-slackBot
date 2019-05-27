class Restaurant():
    cell_indices = {'primary_key':0, 'name':1, 'type':2, 'popular_menu':3, 'price_of_popular_menu':4, 'naver_place_addr':5, 'good':6, 'bad':7}

    def __init__(self, restaurant_info):
        self.restaurant_info = restaurant_info

    def get_info(self):
        return self.restaurant_info

    def get_primary_key(self):
        return self.restaurant_info[Restaurant.cell_indices['primary_key']]

    def get_name(self):
        return self.restaurant_info[Restaurant.cell_indices['name']]
    
    def get_type(self):
        return self.restaurant_info[Restaurant.cell_indices['type']]

    def get_popular_menu(self):
        return self.restaurant_info[Restaurant.cell_indices['popular_menu']]

    def get_price_of_popular_menu(self):
        return self.restaurant_info[Restaurant.cell_indices['price_of_popular_menu']]

    def get_naver_place_addr(self):
        return self.restaurant_info[Restaurant.cell_indices['naver_place_addr']]
    
    def get_good(self):
        return self.restaurant_info[Restaurant.cell_indices['good']]

    def get_bad(self):
        return self.restaurant_info[Restaurant.cell_indices['bad']]
