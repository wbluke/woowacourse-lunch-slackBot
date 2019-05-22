from oauth2client.service_account import ServiceAccountCredentials
import gspread

## credentail init
def init_credentials(json_keyfile_address):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    return ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_address, scope)

## authorize
def get_worksheet_with(credentials, file_name):
    return gspread.authorize(credentials).open(file_name).get_worksheet(0)


class Worksheet():

    def __init__(self, worksheet):
        self.worksheet = worksheet

    def get_table_headers(self):
        return self.worksheet.row_values(1) 

    def get_restaurant_names(self):
        return self.worksheet.col_values(1)[1:]

    def get_all_values(self):
        return self.worksheet.get_all_values()


if __name__ == '__main__':
    credentials = init_credentials(('./woowacourse-lunch-slack-bot.json'))
    worksheet = Worksheet(get_worksheet_with(credentials, "woowacourse-lunch-sheet"))

    table_headers = worksheet.get_table_headers()
    for i in table_headers:
        print(f'{i:<10}', end=' ')
    print()

    restaurant_names = worksheet.get_restaurant_names()
    for i in restaurant_names:
        print(f'{i:<10}', end=' ')
    print()

    all_values = worksheet.get_all_values()
    for i in all_values:
        for j in i:
            print(f'{j:<10}', end=' ')
        print()
