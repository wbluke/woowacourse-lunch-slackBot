from oauth2client.service_account import ServiceAccountCredentials
import gspread
from domain.Restaurant import Restaurant
from pprint import pprint

class GspreadClient():
    def __init__(self, json_keyfile_address, file_name):
        credentials = self.init_credentials(json_keyfile_address)
        worksheet = self.get_worksheet_with(credentials, file_name)
        self.worksheet = worksheet
    
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

    def get_restaurant_row_num_with(self, primary_key):
        return primary_key + 1

    def get_restaurant(self, primary_key):
        restaurant_row_num = self.get_restaurant_row_num_with(primary_key)
        cells = self.worksheet.range(f'A{restaurant_row_num}:H{restaurant_row_num}')
        return Restaurant([cell.value for cell in cells])
    
    def get_num_of_restaurants(self):
        return len(self.worksheet.col_values(1)) - 1

    def get_all_values(self):
        cells = self.worksheet.range(f'A2:H{self.get_restaurant_row_num_with(self.get_num_of_restaurants())}')
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

    def update_good_points_on(self, primary_key, updated_points):
        self.worksheet.update_cell(self.get_restaurant_row_num_with(primary_key), Restaurant.cell_indices['good'] + 1, updated_points)

    def update_bad_points_on(self, primary_key, updated_points):
        self.worksheet.update_cell(self.get_restaurant_row_num_with(primary_key), Restaurant.cell_indices['bad'] + 1, updated_points)
