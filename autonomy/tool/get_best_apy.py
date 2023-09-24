import autonomy as a 

class GetBestApy(a.Tool):
    description = """"Get the best apy between 2 dictionaries"""

    def call(self, data1: dict, data2: dict) -> dict:
        """Get the best apy between 2 dictionaries

        Args:
            data1 (dict): _description_
            data2 (dict): _description_

        Returns:
            market name as a string
        """
        apy1 = data1.get("apy")
        apy2 = data2.get("apy")
        
        if apy1 is None or apy2 is None:
            raise ValueError("One of the dictionaries does not contain the key 'apy'")
        
        if apy1 > apy2:
            return data1['market']
        else:
            return data2['market']

# if __name__ == "__main__":
#     data1={'apy': 3.16061, 'market': 'rocket-pool', 'asset': 'RETH', 'chain': 'Ethereum', 'timestamp': 1695525398.567652}
#     data2={'apy': 4, 'market': 'lido', 'asset': 'RETH', 'chain': 'Ethereum', 'timestamp': 1695525398.567652}
#     apy = GetBestApy()
#     apy.call(data1, data2)
#     print(    apy.call(data1, data2))

