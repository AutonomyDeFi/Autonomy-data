import autonomy as a

class Tool(a.Block):
    name = 'dam'
    description = 'This is a base tool that does nothing.'
    tags = ['defi', 'tool']

    def __init__(
        self,
        **kwargs
    ):
        ## DEFINE TOOL STUFF
        pass

    def call(self, x:int = 1, y:int= 1) -> int:
        return x * 2 + y 
    
    @classmethod
    def info(cls):
        return {
            'name': cls.name,
            'description': cls.description,
            'tags': cls.tags,
            'schema': cls.get_schema('call'),
        }
        
    

    
    
