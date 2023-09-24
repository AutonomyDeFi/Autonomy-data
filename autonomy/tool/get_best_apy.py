def get_best_apy(data1: dict, data2: dict) -> dict:
    if data1["apy"] > data2["apy"]:
        return data1['market']
    else:
        return data2['market']


# if __name__ == "__main__":
#     data1={'apy': 3.16061, 'market': 'rocket-pool', 'asset': 'RETH', 'chain': 'Ethereum', 'timestamp': 1695525398.567652}
#     data2={'apy': 4, 'market': 'lido', 'asset': 'RETH', 'chain': 'Ethereum', 'timestamp': 1695525398.567652}
#     get_best_apy(data1, data2)
#     print(get_best_apy(data1, data2))

