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



class ProcessData():
    def __init__(self, auth, api_url):
        self.auth = auth
        self.api_url = api_url
        self.account_data = self.parse_account_data()
        self.currency_data = self.init_currency_dic()
        self.data_dic = self.create_currency_value_dic()
        self.__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        # self.file = open(os.path.join(__location__, 'data.csv'), 'a+', encoding="utf-8")
        self.file_data = pd.read_csv("data.csv")
    
    def parse_account_data(self):
        # Fetch data from the account (amount of each currencies)
        return requests.get(self.api_url + 'accounts', auth=self.auth).json()

    def init_currency_dic(self):
        currency_data = {}
        currency_data = {
            currency_data['currency']['code']: currency_data['balance']['amount']
                for currency_data in self.account_data['data'] if float(currency_data['balance']['amount']) != 0
        }
        return currency_data
    
    def create_currency_value_dic(self):
        data_dic = {'time': datetime.datetime.now().strftime('%H:%M %d-%m-%Y')}
        for i, cur in enumerate(list(self.currency_data.keys())):
            query = f'prices/{cur}-EUR/buy'
            request_val_price = requests.get(self.api_url + query, auth=self.auth)
            json_price = request_val_price.json()
            price = round(float(json_price['data']['amount']) * float(self.currency_data.get(cur)), 2)
            # Remove if lower than 1 EUR, mainly for DAI
            if price > 1:  
                data_dic[cur] =  price
        
        return data_dic
    
    def save_in_csv(self):
        '''Save the new data in the csv'''
        # directory = os.path.dirname(sys.argv[0])
        if not os.path.isfile('data.csv'):
            print(f"File path 'data.csv' does not exist. Exiting...")
            sys.exit()

        with open(os.path.join(self.__location__, 'data.csv'), 'a+', encoding="utf-8") as file_data:
            csv_writer = csv.writer(file_data)
            csv_writer.writerow(list(self.data_dic.values()))
    


original_values = {
    "DASH": 50,
    "NKN": 50,
    "ANKR": 50,
    "KNC": 50,
    "ADA": 50,
    "MANA": 20,
    "SKL": 32,
    "MATIC": 75,
    "XLM": 50,
    "UNI": 100,
    "LRC": 100,
    "CVC": 100,
    "ETC": 150,
    "XTZ": 50,
    "GRT": 90,
    "ALGO": 100,
    "BCH": 71,
}


def run_pipeline():
    load_dotenv()
    API_KEY = os.getenv("key")
    API_SECRET = os.getenv("secret")
    api_url = 'https://api.coinbase.com/v2/'
    auth = CoinbaseWalletAuth(API_KEY, API_SECRET)  # Config the connection to coinbase
    process = ProcessData(auth, api_url)
    process.save_in_csv()

if __name__ == '__main__':
    run_pipeline()
