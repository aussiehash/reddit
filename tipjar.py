#!/usr/bin/env python3
# [rights]  Copyright 2020 brianddk at github https://github.com/brianddk
# [license] Apache 2.0 License https://www.apache.org/licenses/LICENSE-2.0
# [repo]    https://github.com/brianddk/reddit/tipjar.py
# [btc]     BTC-b32: bc1qwc2203uym96u0nmq04pcgqfs9ldqz9l3mz8fpj
# [tipjar]  https://github.com/brianddk/reddit/tipjar.txt

from requests import get
from re import findall
from time import sleep
from json import dumps

cache = {}
def get_bal(coin):
    uri = coin['uri'].format(**coin)
    coin['addr'] = coin['addr'].lower()
    key = coin['key'].format(**coin)
    if uri not in cache.keys():
        # sleep(1/7)
        r = get(uri)
        cache[uri] = r.json()        
    j = cache[uri]
    for node in key.split('.'):
        if '*' in node:
            _, key, test = node.split(':')
            for node in j:
                if node[key] == test:
                    j = node
                    break
        else:
            j = j[node]
    return float(j) / coin['div'] - coin['dust']

tipjar = dict(
    btc = dict(
        addr = "bc1qwc2203uym96u0nmq04pcgqfs9ldqz9l3mz8fpj,3AAzK4Xbu8PTM8AD3fDnmjdNkXkmu6PS7R,18MDTTiqPM8ZEo29Cig1wfGdkLNtvyorW5",
        uri  = "https://api.blockchair.com/bitcoin/dashboards/addresses/{addr}",
        key  = "data.set.balance",
        dust = 0,
        div  = 10**8,
    ),
    ftc = dict(
        addr = "6mx5WVXsTEdsh9UCainpdAHDrDwH4mZQTD",
        uri  = "https://explorer.feathercoin.com/api/addr/{addr}",
        key  = "balance",
        dust = 0,
        div  = 1,
    ),
    bch = dict(
        addr = "qqz77k4rqar3uppj8k28de06narwkqaamcf624p8zl",
        uri  = "https://api.blockchair.com/bitcoin-cash/dashboards/addresses/{addr}",
        key  = "data.set.balance",
        dust = 0,
        div  = 10**8,
    ),
    xrp = dict(
        addr = "rEXJQNj9frFgG3Wk3smqGFVdMUX53c7Fw4",
        uri  = "https://api.xrpscan.com/api/v1/account/{addr}",
        key  = "xrpBalance",
        dust = 40.0,
        div  = 1
    ),
    ltc = dict(
        addr = "ltc1q5uucgx9f8n70nq7jmjy03rpg84cm4tm70z5rz6,MKcAge42cX6WZnnPfFGJAxReUYZUbsi6t3,LQjSwZLigtgqHA3rE14yeRNbNNY2r3tXcA",
        uri  = "https://api.blockchair.com/litecoin/dashboards/addresses/{addr}",
        key  = "data.set.balance",
        dust = 0,
        div  = 10**8,
    ),
    eth = dict(
        addr = "0xBc72A79357Ff7A59265725ECB1A9bFa59330DB4b",
        uri  = "https://api.blockchair.com/ethereum/dashboards/address/{addr}?erc_20=true",
        key  = "data.{addr}.address.balance",
        dust = 0.00947497,
        div  = 10**18,
    ),
    amb = dict(
        addr = "0xBc72A79357Ff7A59265725ECB1A9bFa59330DB4b",
        uri  = "https://api.blockchair.com/ethereum/dashboards/address/{addr}?erc_20=true",
        key  = "data.{addr}.layer_2.erc_20.*:token_symbol:AMB.balance_approximate",
        dust = 0,
        div  = 1,
    ),
    dai = dict(
        addr = "0xBc72A79357Ff7A59265725ECB1A9bFa59330DB4b",
        uri  = "https://api.blockchair.com/ethereum/dashboards/address/{addr}?erc_20=true",
        key  = "data.{addr}.layer_2.erc_20.*:token_symbol:DAI.balance_approximate",
        dust = 0,
        div  = 1,
    ),
    bat = dict(
        addr = "0xBc72A79357Ff7A59265725ECB1A9bFa59330DB4b",
        uri  = "https://api.blockchair.com/ethereum/dashboards/address/{addr}?erc_20=true",
        key  = "data.{addr}.layer_2.erc_20.*:token_symbol:BAT.balance_approximate",
        dust = 0,
        div  = 1,
    ),
)

for coin in tipjar.keys():
    bal = get_bal(tipjar[coin])
    if bal: print(f"{coin}: {bal:,.8f}")
