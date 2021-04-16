import os, sys
import json, hmac, hashlib, time, requests, csv, datetime, time
import pandas as pd
from requests.auth import AuthBase
from dotenv import load_dotenv

# Create custom authentication for Coinbase API
class CoinbaseWalletAuth(AuthBase):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
        timestamp = str(int(time.time()))
        if request.body:
          message = timestamp + request.method.upper() + request.path_url + request.body
        else:
          message = timestamp + request.method.upper() + request.path_url + ''          
        message_b = bytes(message, 'latin-1')
        signature = hmac.new(bytes(self.secret_key, 'latin-1'), message_b, hashlib.sha256).hexdigest()

        request.headers.update({
          'CB-ACCESS-SIGN': signature,
          'CB-ACCESS-TIMESTAMP': timestamp,
          'CB-ACCESS-KEY': self.api_key,
        })
        return request


def create_currency_list(account_data):
    currency_list = []
    
    currency_list = [
        currency_data['currency']['code'] for currency_data in account_data['data'] if float(currency_data['balance']['amount']) != 0
    ]
    return currency_list
  
def init_currency_dic(account_data):
    currency_data = {}
    
    currency_data = {
        currency_data['currency']['code']: currency_data['balance']['amount'] for currency_data in account_data['data'] if float(currency_data['balance']['amount']) != 0
    }
    return currency_data


def create_currency_value_dic(currency_list, currency_amount_dic, api_url, auth):
    data_dic = {'time': datetime.datetime.now().strftime('%H:%M %d-%m-%Y')}

    for i, cur in enumerate(currency_list):
        query = f'prices/{cur}-EUR/buy'
        request_val_price = requests.get(api_url + query, auth=auth)
        json_price = request_val_price.json()
        data_dic[cur] = round(float(json_price['data']['amount']) * float(currency_amount_dic.get(cur)), 2)
    
    return data_dic


def save_in_csv(data_dic):
    '''Save the new data in the csv'''
    # directory = os.path.dirname(sys.argv[0])
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    if not os.path.isfile('data.csv'):
        print(f"File path 'data.csv' does not exist. Exiting...")
        sys.exit()

    with open(os.path.join(__location__, 'data.csv'), 'a+', encoding="utf-8") as file_data:
        csv_writer = csv.writer(file_data)
        csv_writer.writerow(list(data_dic.values()))


def run_pipeline():
    load_dotenv()
    API_KEY = os.getenv("key")
    API_SECRET = os.getenv("secret")
    api_url = 'https://api.coinbase.com/v2/'
    auth = CoinbaseWalletAuth(API_KEY, API_SECRET)  # Config the connection to coinbase
    account_data = requests.get(api_url + 'accounts', auth=auth).json()  # Fetch data from the account (amount of each currencies)
    currency_list = create_currency_list(account_data)
    currency_amount_dic = init_currency_dic(account_data)
    data_dic = create_currency_value_dic(currency_list, currency_amount_dic, api_url, auth)  # Format the data into a dic, with currency tags as keys and amount (EUR) as values
    save_in_csv(data_dic)

if __name__ == '__main__':
    run_pipeline()
