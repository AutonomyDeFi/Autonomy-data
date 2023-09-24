import requests 
import json
from typing import Optional, Dict, Any
import time
from typing import *

import os
from dotenv import load_dotenv
from web3 import Web3
import autonomy as a

from dotenv import load_dotenv

class InchPrices(a.Tool):
    description = """

    Gets the token prices from the 1inch API.

    params: A list of token addresses.
    return: A dictionary of token addresses and prices.

    """
    def __init__(self, 
                 api_key: Optional[str] = 'INCH_API_KEY',
                url: Optional[str] = "https://api.1inch.dev/price/v1.1/1"
                 ):
        self.api_key = os.getenv(api_key, api_key)
        self.url = url

        self.token_mappings = {
        "usdc": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        "wsteth": "0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0",
        "reth": "0xae78736cd615f374d3085123a210448e74fc6393",
        "dai": "0x6b175474e89094c44da98b954eedeac495271d0f",
        "usdt": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "wbtc": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
        "weth": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
    }


    def call(self, tokens: List[str]= ['weth']) -> dict[str, float]:

        for i,t in enumerate(tokens):
            if t.lower() in self.token_mappings:
                tokens[i] = self.token_mappings.get(t.lower())           
        print(tokens)

        payload = {
            "tokens": tokens
        }

        response = requests.post(self.url, json=payload, headers={'Authorization': f'Bearer {self.api_key}'})
        print(response)
        if response.status_code == 200:
            prices = response.json()
            print("Prices for requested tokens:")
            for token_address, price in prices.items():
                print(f"{token_address}: {price}")
        else:
            print("Failed to fetch token prices.", response.text)
