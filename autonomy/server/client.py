

from typing import Tuple, List, Union
import asyncio
import autonomy as a
import aiohttp
import json


class Client(a.Block):

    def __init__( self, address: str , network: str ='local'):

        namespace = a.namespace(network=network)
        address = namespace.get(address, address)
        self.loop = a.get_event_loop()
        self.address = address 
        ip = address.split(':')[0]
        self.serializer = a.block('server.serializer')()
        ip, port = address.split(':')
        self.ip = ip 
        self.port = port
        
    async def async_forward(self,
        fn: str,
        args: list = None,
        kwargs: dict = None,
        timeout: int = 4,
        headers : dict ={'Content-Type': 'application/json'}):


        args = args if args else []
        kwargs = kwargs if kwargs else {}

        url = f"http://{self.address}/{fn}/"

        request_data =  { 
                        "args": args,
                        "kwargs": kwargs,
                        }
        
        request_data = self.serializer.serialize( request_data)
        request = {'data': request_data}

        a.print(request)

        result = '{}'
        # start a client session and send the request
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=request, headers=headers) as response:
                if response.content_type == 'text/event-stream':
                    # Process SSE events
                    result = ''
                    async for line in response.content:
                        # remove the "data: " prefix
                        event_data = line.decode('utf-8').strip()[len('data: '):]
                        result += event_data
                    result = json.loads(result)
                elif response.content_type == 'application/json':
                    result = await asyncio.wait_for(response.json(), timeout=timeout)
                elif response.content_type == 'text/plain':
                    # result = await asyncio.wait_for(response.text, timeout=timeout)
                    a.print(response.text)
                    result = json.loads(result)
                else:
                    raise ValueError(f"Invalid response content type: {response.content_type}")
        # process output 
        result = self.process_output(result)
        
        return result

    def process_output(self, result):
        ## handles 
        result = self.serializer.deserialize(result)['data']
        return result 
        
    def forward(self,
                fn:str,
                args=None, 
                kwargs=None,
                return_future:bool=False, 
                timeout:str=4):
        forward_future = asyncio.wait_for(self.async_forward(fn=fn, args=args, kwargs=kwargs), timeout=timeout)
        if return_future:
            return forward_future
        else:
            return self.loop.run_until_complete(forward_future)
        
    def __str__ ( self ):
        return "Client({})".format(self.address) 
    def __repr__ ( self ):
        return self.__str__()
    def __exit__ ( self ):
        self.__del__()


    def test_module(self):
        module = Client(ip='0.0.0.0', port=8091)
        import torch
        data = {
            'bro': torch.ones(10,10),
            'fam': torch.zeros(10,10)
        }


