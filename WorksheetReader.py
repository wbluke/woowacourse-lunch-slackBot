from oauth2client.service_account import ServiceAccountCredentials
import gspread



JSON_KEYFILE_ADDRESS = 'lunchBot-worksheet-key.json'
SHEET_NAME = 'woowacourse-lunch-sheet'

class Worksheet():
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

    def get_restaurant(self, restaurant_number):
        return Restaurant(self.worksheet.row_values(restaurant_number + 1))

    def get_table_headers(self):
        return self.worksheet.row_values(1)

    def get_all_restaurant_names(self):
        return self.worksheet.col_values(1)[1:]
    
    def get_all_values(self):
        return self.worksheet.get_all_values()


class Restaurant():
    def __init__(self, restaurant_info):
        self.restaurant_info = restaurant_info

    def get_name(self):
        return self.restaurant_info[1]
    
    def get_type(self):
        return self.restaurant_info[2]

    def get_popular_menu(self):
        return self.restaurant_info[3]

    def get_price_of_popular_menu(self):
        return self.restaurant_info[4]

    def get_naver_place_addr(self):
        return self.restaurant_info[5]
    
    def get_good(self):
        return self.restaurant_info[6]

    def get_bad(self):
        return self.restaurant_info[7]


if __name__ == '__main__':
    worksheet = Worksheet(JSON_KEYFILE_ADDRESS, SHEET_NAME)

    table_headers = worksheet.get_table_headers()
    for i in table_headers:
        print(f'{i:<10}', end=' ')
    print()

    restaurant_names = worksheet.get_all_restaurant_names()
    for i in restaurant_names:
        print(f'{i:<10}', end=' ')
    print()

    all_values = worksheet.get_all_values()
    for i in all_values:
        for j in i:
            print(f'{j:<10}', end=' ')
        print()
