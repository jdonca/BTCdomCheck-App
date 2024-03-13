
import csv
import sys
from datetime import datetime
import requests
import zipfile
import os
import re
import numpy as np

def main():
    date, init_pair_i, init_pair_ii = pair_date()

    i = input('Please seleft from these options: ' + '\n' +
    'Press "1" to get historic data' + '\n'
    'Press "2" to sell stable coin purchase against BTC' + '\n')
    print('')

    if i == '1':
        stable_pair = init_pair_i + init_pair_ii
        stable_pair_historic = print_(get_historic(date, stable_pair), date, stable_pair)
        print(stable_pair_historic)

    else:
        init_pair_in_btc = init_pair_i + 'BTC'
        i_symbols = get_symbols()

        if not any(d['symbol'] == init_pair_in_btc for d in i_symbols):
            print(f'{init_pair_i} does not have a BTC pair\nPlease try again with a different coin')
            main()
        else:
            btc_pair_historic = get_historic(date, init_pair_in_btc), date, init_pair_in_btc
            btc_pair_current = float(get_current(init_pair_in_btc))
            historic_price = float(btc_pair_historic[0])

            avg = average(historic_price, float(btc_pair_current))

            btc_pair_historic = print_(historic_price, date, init_pair_in_btc)
            print(btc_pair_historic)
            print_(btc_pair_current)

            if historic_price > btc_pair_current:
                print(f'Current loss is at -%{abs(avg):.2f}')

            else:
                print(f'Current gain is at %{avg:.2f}')


def pair_date():
    while True:
        try:
            date = input('Date in format dd/mm/yyyy: ').strip()
            matches = re.search(r'(\d\d?)\/(\d\d?)\/(\d{4})', date)
            if matches:
                init_pair_i, init_pair_ii = pair_input()
                print('')
                return date, init_pair_i, init_pair_ii
            else:
                print('Not a valid date')
        except EOFError:
            sys.exit('\nVuelva prontos')

def get_symbols():
    url = 'https://api.binance.com/api/v1/exchangeInfo'
    r = requests.get(url)
    get_data = r.json()
    i_symbols = get_data['symbols']
    return i_symbols

def pair_input():
    i_symbols = get_symbols()
    pair = ''
    while pair == '':
        while True:
            try:
                i = input('Base: ' ).upper().strip()
                if not any(d['baseAsset'] == i for d in i_symbols):
                    print('Not a valid base')
                else:
                    break
            except EOFError:
                sys.exit('\nVuelva prontos')

        while True:
            try:
                ii = input('Quote: ').upper().strip()
                if not any(d['quoteAsset'] == ii for d in i_symbols):
                    print('Not a valid quote symbol')
                else:
                    break
            except EOFError:
                sys.exit('\nVuelva prontos')

        try:
            test_pair = i + ii
            if not any(d['symbol'] == test_pair for d in i_symbols):
                print('Not a valid pair')
            else:
                pair += test_pair
                break
        except EOFError:
            sys.exit('\nVuelva prontos')

    return i, ii


def print_(price=0, date=None, pair=None):
    if date is None and pair is None:
        return print(f'Current price of your coin in BTC is', np.format_float_positional(float(price), trim='-'), 'BTC')

    if len(pair) > 4 and pair[-3:] == 'BTC':
        text = f'The open price for the pair {pair} on {date} was {np.format_float_positional(float(price))} BTC'
        return text

    else:
        text = f'The open price for the pair {pair} on {date} was ${float(price):.2f}'
        return text


def get_historic(date_input, pair_input):
    matches = re.search(r'(\d\d?)\/(\d\d?)\/(\d{4})', date_input)
    if matches:
        d, m, year = matches.groups()
        day = d.zfill(2)
        month = m.zfill(2)

    url = f'https://data.binance.vision/data/spot/monthly/klines/{pair_input}/1d/{pair_input}-1d-{year}-{month}.zip'
    r = requests.get(url,stream=True)

    if r.status_code == 404:
        print('\nThere is no data for this pair, please try again with a more recent date.')
        main()
        sys.exit(0)

    zip_file_name  = url.split("/")[-1]
    open(zip_file_name, 'wb').write(r.content)

    csv_file_name = ''
    with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
        zip_ref.extractall()
        extracted = zipfile.ZipFile.namelist(zip_ref) # get extracted filename
        csv_file_name += extracted[0] # list to string

    kline = []
    price = ''

    with open(csv_file_name) as data:
        reader = csv.reader(data)
        while True:
            for row in reader:
                open_time, open_price, high, low, close, close_time = int(row[0]), row[1], row[2], row[3], row[4], row[6]
                #time_stamp = open_time / 1000
                dt_open_time = datetime.fromtimestamp(open_time / 1000)
                str_open_time = dt_open_time.strftime('%d')

                if day == str_open_time:
                    price += open_price
                    os.remove(csv_file_name)
                    os.remove(zip_file_name)
                    return price


def get_current(pair):
    url = f'https://api.binance.com/api/v1/ticker/price?symbol={pair}'
    r = requests.get(url,stream=True)
    get_data = r.json()
    return get_data['price']

def average(hist, current):
    return ((current - hist) / hist) * 100

if __name__ == "__main__":
    main()