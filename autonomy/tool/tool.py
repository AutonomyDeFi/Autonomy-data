import autonomy as a

class Tool(a.Block):
    name = None
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
            'name': cls.name if cls.name else cls.block_name(),
            'description': cls.description,
            'tags': cls.tags,
            'schema': cls.get_schema('call'),
        }
    
    @classmethod
    def tool2info(self):
        for tool in a.tools(info=True):
            print(tool.info())
    
    @classmethod
    def tool2info(cls):
        tools = a.tools()
        tool2info = {}
        for tool in tools:
            tool_info = a.block(tool).info()
            tool2info[tool_info['name']] = tool_info
        return tool2info
    
    

    
    
