import autonomy as a

class Tool(a.Tool):
    description = 'This is a base tool that does nothing.'
    tags = ['defi', 'tool']
    def __init__(
        self,
        **kwargs
    ):
        a.Tool.__init__(self, **kwargs)
    
    def call(self, **kwargs) -> int:
        return kwargs
    
