
from typing import Dict, List, Optional, Union
import autonomy as a
from .serializer import Serializer
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

class ServerHttp(a.Block):
    def __init__(
        self,
        block: a.Block,
        name : str = None,
        tag = None,
        port: Optional[int] = 8888,
        ip: Optional[str] = '0.0.0.0',
        network: Optional[str] = 'local',
        ):

        self.serializer = a.block('server.serializer')()
        self.ip = ip
        self.port = port
        self.address = f"{self.ip}:{self.port}"
        self.block = block
        self.name = self.resolve_name(name=name, tag=tag)
        self.network = network


        self.set_api(ip=self.ip,
                     port=self.port)

    def resolve_name(self, name:str = None, tag:str=None):
        if name == None:
            if hasattr(self.block, 'block_name'):
                name = self.block.block_name()
            else:
                name = self.block.__name__.lower()
        if tag != None:
            name = f'{name}::{tag}'
        return name

    def set_api(self, ip:str, port:int,):

        self.app = FastAPI()
        self.app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )


        @self.app.post("/{fn}")
        async def forward_api(fn:str, input:dict):
            address_abbrev = None
            try:

                input['fn'] = fn

                input = self.process_input(input)

                data = input['data']
                args = data.get('args',[])
                kwargs = data.get('kwargs', {})
                
                result = self.forward(fn=fn,
                                    args=args,
                                    kwargs=kwargs,
                                    )

                success = True
            except Exception as e:
                raise e
                result = c.detailed_error(e)
                success = False
            
            result = self.process_result(result)
            

            if success:
                
                a.print(f'\033[32m Success: {self.name}::{fn} 🎉\033 ')
            else:
                a.print(result)
                a.print(f'\033🚨 Error: {self.name}::{fn} 🚨\033')

            return result
        
        self.start()
        
        
    def process_input(self,input: dict) -> bool:
        input['data'] = self.serializer.deserialize(input['data'])
        return input


    def process_result(self,  result):

        result = self.serializer.serialize({'data': result})
        return result
        
    


    def start(self, **kwargs):
        import uvicorn

        try:
            a.print(f'\033🚀 Serving {self.name} on {self.address} 🚀\033')
            self.register_server(name=self.name, address=self.address)
            uvicorn.run(self.app, host=self.ip, port=self.port)
        except Exception as e:
            a.print(e, color='red')
        finally:
            self.deregister_server(self.name)
        

    def forward(self, fn: str, args: List = None, kwargs: Dict = None, **extra_kwargs):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}

        obj = getattr(self.block, fn)

        if callable(obj):
            response = obj(*args, **kwargs)
        else:
            response = obj
        return response

    def register_server(self, name:str, address:str):
        '''
        Register a block in the namespace
        '''
        return a.block('server.namespace').register_server(name, address, network=self.network)
    

    def deregister_server(self, name:str):
        '''
        Register a block in the namespace
        '''

        return a.block('server.namespace').deregister_server(name, network=self.network)
    
    @classmethod
    def networks(cls):
        '''
        Get a list of networks
        '''
        return a.block('server.namespace').networks()
