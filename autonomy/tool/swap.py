import autonomy as a    


class SwapTool(a.Tool):
    description = """
    Swaps tokens on Uniswap.
    params:
        tokenin: str = 'ETH'
        token_out: str = 'USDC'
        amount: int = 100
    returns:
        result: dict
    """

    def call(self, tokenin: str = 'ETH', token_out: str = 'USDC', amount: int = 100):
        self.tokenin = tokenin
        self.token_out = token_out
        self.amount = amount
        return {'result': f'Swapped {amount} {tokenin} for {token_out}'}
