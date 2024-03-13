# BTCdomCheck App
    #### Video Demo:  https://youtu.be/22erSzFYCbM
    #### Description: Final project for CS50P

# Introduction
This is the final project for Harvard X program CS50P, 'Introduction to Python'. My very first programming course, at age 39 and with a 3 yr old son, I finally put hands on to the scary color lines and dream of writing good and useful code.
#

## Table of contents
* [Libraries](#libraries)
* [Endpoints](#endpoints)
* [Documentation](#documentation)
* [General info](#general-info)
* [Little story behind this](#a-little-history-behind-it)
* [Features](#features)
* [Silly things that slowed me down](#silly-things-that-slowed-me-down)
* [Project status](#project-status)
* [Demo!]
#
## Libraries
The following libraries has been used for this project:
- csv
- datetime
- requests
- zipfile
- os
- re
- numpy
#
## Endpoints

```
https://api.binance.com/api/v1/ticker/price?symbol={pair}

https://data.binance.vision/data/spot/monthly/klines/{pair_input}/1d/{pair_input}-1d-{year}-{month}.zip

https://api.binance.com/api/v1/exchangeInfo
```
#

## Documentation
This is the official documentation from Binance, and what was used to develop this project.

https://www.binance.com/en/binance-api
https://www.binance.com/en/landing/data
https://data.binance.vision/?prefix=data/spot/daily/klines/

#
## General info
The purpose of this program is to get historical crypto data, from Binance exchange. But more specific, to know if we can get out of a coin that was bought against a stable pair (USDT, USDC, DAI...), and price dropped drastically,
but perhaps it hasn't lost value against BTC (or even gained value!). BTC dominance, being the key factor.
#
## A little history behind it :) 
On 2018 I bought some bitcoin, then one year later I bought some more. Then I forgot about it.
Year 2020 coming to an end, and BTC was going over 20K again (and fast!). Started investigating, and around beginning of may I was buying a bit of everything :P then BTC collapsed to 28K and the whole market went down.

It's when I noticed some coins would outperform BTC, so selling the same coin I bought with US dollars, but now against BTC would allow me break even or get a little profit (if you believe that BTC will recover).

To do this, you have to go to the day you bought the coin, check the price, then check same coin but the BTC pair now, go to purchase date to find the price at that moment (now in BTC). Finally check current price on BTC pair and decide if you are in profit or loss.

This is what this little program does for you!
#
## Features
- Get historic data from Binance, up to year 2017
- Open price for specific day, daily candle
- Get a stable coin pair, valued on BTC according to date of purchase and current value
- Percentage of gain or loss for BTC conversion
- Symbol validation, if input coin does not have a BTC pair, the program will flag it
#
## Silly things that slowed me down
Along the way, what seemed simple things like returning a value in BTC, took me (way!) longer than expected.
- Scientific notation

    Python automatically represents a very small number in scientific notation, and this was messing up with calculations, validation of lenght (for instance, '0.00004' would be converted to '4e-5').

    **Numpy** was a nice solution to this. This simple line will convert from scientific to decimal:
    ```
    import numpy as np

    np.format_float_positional(float({price})
    ```
- Validate Binance list of coins and pairs

    Getting the list is not difficult, but having to validate on severdal different places of my code made it difficult to not over extend in lines, making `for`loops everywhere.
    This one liner provided by user https://stackoverflow.com/users/61974/mark-byers was very helpful!

    [Link to the answer](https://stackoverflow.com/questions/3897499/check-if-value-already-exists-within-list-of-dictionaries#:~:text=Here%27s%20one%20way%20to%20do%20it%3A)

    Example from the post and solution:
    ```
    a = [
    {'main_color': 'red', 'second_color':'blue'},
    {'main_color': 'yellow', 'second_color':'green'},
    {'main_color': 'yellow', 'second_color':'blue'},
    ]
    ```
    ```
    if not any(d['main_color'] == 'red' for d in a):
    # does not exist
    ```

    On my code created a function to get the symbols:

    ```
    def get_symbols():
        url = 'https://api.binance.com/api/v1/exchangeInfo'
        r = requests.get(url)
        get_data = r.json()
        i_symbols = get_data['symbols']
        return i_symbols
    ```
    The for loop to validate (one of the appearances):

    ```
    i_symbols = get_symbols()

    if not any(s['symbol'] == init_pair_in_btc for s in i_symbols):
        print(f'{init_pair_i} does not have a BTC pair\nPlease try again with a different coin')
    ```
# Project status
This project could be much much bigger and I had so many different ideas, but I had to deliver it some day so I can move on to the next course :)

I may (or may not), add new functionalities I had in mind like:
- DCA and average price

    Be able to input several purchases, when and how much invested. Then the program will deliver a calculated average price
- Save the DCA data on a CSV file, formatted with columns and rows, with the possibility of coming back to keep adding stuff to it
- Print a table on the screen (console) with the results (list of purchases and final average price)
- Add triggers, like email me when certain coin has gone up or down by x%
- I could keep adding stuff on and on, that YES they already exists, but they are paid, or have to install some software to get it, or or or...

    The purpose of all this is to work with APIs rather than a GUI that can fail, or slow things down (aka Binance not responding when abrupt market movements occurs... you would know if ever operated the Binance Futures market)
#

## Demo
And finally, a demo, yaaay! :P
[Demo time!](https://youtu.be/22erSzFYCbM)
