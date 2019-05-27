from oauth2client.service_account import ServiceAccountCredentials
import gspread
from domain.Restaurant import Restaurant
from pprint import pprint

class GspreadClient():
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
        cells = self.worksheet.range(f'A2:H{self.num_of_restaurants + 1}')
        num_of_restaurant_cell_indices = len(Restaurant.cell_indices)

        list_of_list = []
        for idx in range(0, len(cells), num_of_restaurant_cell_indices):
            list_of_list.append([cell.value for cell in cells[idx:idx + num_of_restaurant_cell_indices]])

        list_of_values = []
        for values in list_of_list:
            list_of_values.append(list(map(lambda value: int(value) if value.isdigit() else value, values)))
        
        return list_of_values

    def get_all_restaurants(self):
        list_of_values = self.get_all_values()

        return [Restaurant(row) for row in list_of_values]

    def increase_one_good_point_on_key_no(self, cell_primary_key, updated_points):
        pass

    def increase_one_bad_point_on_key_no(self, cell_primary_key, updated_points):
        pass
