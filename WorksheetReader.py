from oauth2client.service_account import ServiceAccountCredentials
import gspread

JSON_KEYFILE_ADDRESS = 'lunchBot-worksheet-key.json'
SHEET_NAME = 'woowacourse-lunch-sheet'

class Worksheet():
    def __init__(self, json_keyfile_address, file_name):
        credentials = self.init_credentials(json_keyfile_address)
        worksheet = self.get_worksheet_with(credentials, file_name)
        self.worksheet = worksheet
        self.num_of_restaurants = len(self.worksheet.col_values(1)) - 1
    
    ## credential init
    def init_credentials(self, json_keyfile_address):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        return ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_address, scope)

    ## authorize and get worksheet
    def get_worksheet_with(self, credentials, file_name):
        return gspread.authorize(credentials).open(file_name).get_worksheet(0)

    def get_table_headers(self):
        return self.worksheet.row_values(1)

    def get_all_restaurant_names(self):
        return self.worksheet.col_values(2)[1:]

    def get_restaurant(self, restaurant_number):
        cells = self.worksheet.range(f'A{restaurant_number + 1}:H{restaurant_number + 1}')
        return Restaurant([cell.value for cell in cells])
    
    def get_num_of_restaurants(self):
        return self.num_of_restaurants

    def get_all_values(self):
        cells = self.worksheet.range(f'A2:H{self.num_of_restaurants}')
        num_of_restaurant_cell_indices = len(Restaurant.cell_indices)

        list_of_values = []
        values = []
        cell_count = 0
        for cell in cells:
            values.append(cell.value)
            cell_count += 1
            if (cell_count % num_of_restaurant_cell_indices == 0):
                list_of_values.append(values)
                values = []
        return list_of_values

    def get_all_restaurants(self):
        list_of_values = self.get_all_values()
        restaurants = []
        for row in list_of_values:
            restaurants.append(Restaurant(row))
        return restaurants

    def increase_one_good_point_on_key_no(self, cell_primary_key, updated_points):
        pass

    def increase_one_bad_point_on_key_no(self, cell_primary_key, updated_points):
        pass


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


if __name__ == '__main__':
    worksheet = Worksheet(JSON_KEYFILE_ADDRESS, SHEET_NAME)

    all_restaurants = worksheet.get_all_restaurants()
    for restaurant in all_restaurants:
        print(f'{restaurant.get_name():<10}  {restaurant.get_popular_menu():<10}  {restaurant.get_price_of_popular_menu():<10}')

    print(f'count : {worksheet.get_num_of_restaurants()}')

    r = worksheet.get_restaurant(5)
    for item in r.get_info():
        print(item, end=' ')
    print()