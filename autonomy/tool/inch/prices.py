import requests 
import json
from typing import Optional, Dict, Any
import time

import os
from dotenv import load_dotenv
from web3 import Web3
import autonomy as a


class InchPrices(a.Tool):
    description = """

    Gets the token prices from the 1inch API.

    params: A list of token addresses.
    return: A dictionary of token addresses and prices.

    """
    def __init__(self, 
                 api_key: Optional[str] = '1INCH_API_KEY',
                url: Optional[str] = "https://api.1inch.dev/price/v1.1/1"
                 ):
        self.api_key = os.getenv(api_key, api_key)
        self.url = url


    def call(self, tokens:list[str]) -> dict[str, float]:

        payload = {
            "tokens": tokens
        }

        response = requests.post(self.url, json=payload)
        if response.status_code == 200:
            prices = response.json()
            print("Prices for requested tokens:")
            for token_address, price in prices.items():
                print(f"{token_address}: {price}")
        else:
            print("Failed to fetch token prices.")
