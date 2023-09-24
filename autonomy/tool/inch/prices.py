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
                 api_key: Optional[str] = 'INCH_API_KEY',
                url: Optional[str] = "https://api.1inch.dev/price/v1.1/1"
                 ):
        self.api_key = os.getenv(api_key, api_key)
        self.url = url

        self.token_mappings = {
            "cusdcv3": "0x3EE77595A8459e93C2888b13aDB354017B198188",
            "cwethv3": "0x9A539EEc489AAA03D588212a164d0abdB5F08F5F",
            "usdc": "0x07865c6E87B9F70255377e024ace6630C1Eaa37F",
            "wbtc": "0xAAD4992D949f9214458594dF92B44165Fb84dC19",
            "weth": "0x42a71137C09AE83D8d05974960fd607d40033499"
        }


    def call(self, tokens:list[str] = ['eth']) -> dict[str, float]:
        for i,t in enumerate(tokens):
            print(t)
            tokens[i] = self.token_mappings.get(t.lower())           
        print(tokens)

        payload = {
            "tokens": tokens
        }

        response = requests.post(self.url, params=payload, headers={'Authorization': f'Bearer {self.api_key}'})
        print(response)
        if response.status_code == 200:
            prices = response.json()
            print("Prices for requested tokens:")
            for token_address, price in prices.items():
                print(f"{token_address}: {price}")
        else:
            print("Failed to fetch token prices.", response.text)

    def test(self):
        self.call(["0x42a71137C09AE83D8d05974960fd607d40033499"])
