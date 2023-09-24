
import os
from typing import *

class a(object):
    root_path = os.path.dirname(os.path.realpath(__file__))
    homepath = os.path.expanduser('~')
    library_name = 'autonomy'
    network = 'local'
    pwd = os.getenv('PWD') #  
    home = os.path.expanduser('~') # the home directory
    __ss58_format__ = 42 # the ss58 format for the substrate address


    @classmethod
    def agents(cls, search: str= None) -> list:
        agents =  a.blocks('agent')
        if search != None:
            agents = [a for a in agents if search in t]
        return agents
    


    @classmethod
    def python_paths(cls, path=root_path) -> List[str]:
        from glob import glob
        # find all of the python files
        paths = []
        for f in glob(a.root_path + '/**/*.py', recursive=True):
            if os.path.isdir(f):
                continue

            paths.append(f)
        return paths
    
    @staticmethod
    def path2name(path):
        name = path.replace(a.root_path+'/', '').replace('.py','').replace('/','.')
        name_splits =  list(name.split('.'))
        new_name = []
        for name_split in name_splits:
            if name_split not in new_name:
                new_name.append(name_split)
        name = '.'.join(new_name)
        return name
    

    @classmethod
    def name2path(cls):
        paths = cls.python_paths()
        name2path = {}
        for p in paths:
            name = p.replace(a.root_path+'/', '').replace('.py','').replace('/','.')
            name_splits =  list(name.split('.'))

            new_name = []
            for name_split in name_splits:
                if name_split not in new_name:
                    new_name.append(name_split)
            name = '.'.join(new_name)
            
            classes = a.find_python_class(p)
            if len(classes) > 0:
                name2path[name] = p
        del name2path['block']
        return name2path

    @classmethod
    def name2importpath(cls):
        name2path = cls.name2path()
        name2importpath = {}
        for name, path in name2path.items():
            block_classes = a.find_python_class(path)
            if len(block_classes) > 0:
                block_class = block_classes[0]
                name2importpath[name] =  a.root_path.split('/')[-1] + '.' + path.replace(a.root_path+'/', '').replace('.py','').replace('/','.') +  '.' + block_class
        return name2importpath
    

    @classmethod
    def test(cls):
        print(a.tools())
    
    @classmethod
    def find_python_class(cls, path:str , class_index:int=0, search:str = None, start_lines:int=2000):
        import re
        
        # read the contents of the Python script file
        python_script = a.get_text(path)
        class_names  = []
        lines = python_script.split('\n')
        
        for line in lines:

            key_elements = ['class ', '):', '(']
            self_ref_condition = 'key_elements' not in line

            has_class_bool = all([key_element in line for key_element in key_elements])

            if has_class_bool:
                if  search != None:
                    if isinstance(search, str):
                        search = [search]
                    if not any([s in line for s in search]):
                        continue
                        
                class_name = line.split('class ')[-1].split('(')[0].strip()
                class_names.append(class_name)
                
        # return the class names
        return class_names
    

    @classmethod
    def get_json(cls, path:str,  **kwargs):
        import json
        path = cls.resolve_path(path)
        return json.loads(cls.get_text(path, **kwargs))
    
    @classmethod
    def put_json(cls, path:str, data:dict, **kwargs):
        import json
        path = cls.resolve_path(path)
        return cls.put_text(path, json.dumps(data), **kwargs)
    
    @classmethod
    def put(cls, path:str, data:str, **kwargs):
        path = cls.resolve_path(path)
        return cls.put_json(path, {'data': data}, **kwargs)
    
    @classmethod
    def get(cls, path:str, default=None,  **kwargs):
        path = cls.resolve_path(path)
        if not os.path.exists(path):
            data = {} if default == None else default
            return data
        data =  cls.get_json(path, **kwargs)
        return data['data']
    
    
    @classmethod
    def ls(cls, path:str = '', 
           recursive:bool = False):
        path = cls.resolve_path(path)
        try:
                ls_files =  os.listdir(path)
        except FileNotFoundError as e:
            a.print(f'Path {path} does not exist')
            return []
        ls_files = [os.path.expanduser(os.path.join(path,f)) for f in ls_files]
        return ls_files
    
    @classmethod
    def exists(cls, path:str) -> bool:
        path = cls.resolve_path(path)
        return os.path.exists(path)

    @classmethod
    def put_text(cls, path:str, text:str) -> None:
        import os
        # Get the absolute path of the file
        path = cls.resolve_path(path)
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        # Write the text to the file
        with open(path, 'w') as file:
            file.write(text)

        return {'success': True, 'path': path, 'msg': f'Wrote text to {path}'}

    @classmethod
    def get_text(cls, 
                 path: str, 
                 start_byte:int = 0,
                 end_byte:int = 0,
                 start_line :int= None,
                 end_line:int = None,
                  root=False, ) -> str:
        # Get the absolute path of the file
        
        # Read the contents of the file
        with open(path, 'rb') as file:
        
                
            file.seek(0, 2) # this is done to get the fiel size
            file_size = file.tell()  # Get the file size
            if start_byte < 0:
                start_byte = file_size - start_byte
            if end_byte <= 0:
                end_byte = file_size - end_byte 
            chunk_size = end_byte - start_byte + 1
            file.seek(start_byte)
            content_bytes = file.read(chunk_size)
            try:
                content = content_bytes.decode()
            except UnicodeDecodeError as e:
                if hasattr(content_bytes, 'hex'):
                    content = content_bytes.hex()
                else:
                    raise e
                
            if start_line != None or end_line != None:
                
                content = content.split('\n')
                if end_line == None or end_line == 0 :
                    end_line = len(content) 
                if start_line == None:
                    start_line = 0
                if start_line < 0:
                    start_line = start_line + len(content)
                if end_line < 0 :
                    end_line = end_line + len(content)
                content = '\n'.join(content[start_line:end_line])

        return content
    
    @classmethod
    def blocks(cls, search = None):
        blocks =  list(a.name2path().keys())
        if search != None:
            blocks = [b for b in blocks if search in b]
        return blocks
    
    
    @classmethod
    def import_block(cls, block) -> 'Block': 
        name2path =  a.name2importpath()
        path =  name2path[block]
        return a.import_object(path)
    

    @classmethod
    def import_object(self, path:str) -> 'Block':
        import importlib
        object_name = path.split('.')[-1]
        path = '.'.join(path.split('.')[:-1])
        module = importlib.import_module(path)
        obj = getattr(module, object_name)
        return obj
    
    @classmethod
    def get_function_annotations(cls, fn) -> dict:
        fn = cls.resolve_fn(fn)
        return fn.__annotations__

    @classmethod
    def resolve_fn(cls, fn):
        if isinstance(fn, str):
            fn = getattr(cls, fn)
        assert callable(fn), f'{fn} is not callable'
        return fn
    

    @classmethod
    def get_schema(cls, fn:str)->dict:
        '''
        Get function schema of function in cls
        '''
        fn_schema = {}
        fn = cls.resolve_fn(fn)
        fn_schema['input']  = cls.get_function_annotations(fn=fn)

        for k,v in fn_schema['input'].items():
            v = str(v)
            if '<class ' in v:
                fn_schema['input'][k] =  str(v.split("<class '")[-1].split("'")[0])
            fn_schema['input'][k] = str(v)
        fn_schema['output'] = fn_schema['input'].pop('return', None)
        
        fn_schema['default'] = cls.get_function_defaults(fn=fn) 
        for k,v in fn_schema['default'].items(): 
            if k not in fn_schema['input'] and v != None:
                fn_schema['input'][k] = type(v).__name__ if v != None else None



        return fn_schema
    
    @classmethod
    def get_function_defaults(cls, fn:str):
        import inspect
        fn = cls.resolve_fn(fn)
        function_defaults = dict(inspect.signature(fn)._parameters)
        for k,v in function_defaults.items():
            if v._default != inspect._empty and  v._default != None:
                function_defaults[k] = v._default
            else:
                function_defaults[k] = None
        function_defaults.pop('self', None)
        function_defaults.pop('cls', None)
        return function_defaults
    
    @classmethod
    def block(cls, block:str):
        return a.import_block(block)
    
    @classmethod
    def print(cls, *args, **kwargs):
        from rich.console import Console
        if not hasattr(cls, 'console'):
            cls.console = Console()

        return cls.console.print(*args, **kwargs)
    
    @classmethod
    def cli(cls, *args, **kwargs):
        return a.block('cli')(*args,**kwargs)

    @classmethod
    def fns(cls, search:str = None):
        return []
    
    @classmethod
    def schema(cls,search: str = None, **kwargs) -> 'Schema':
        return {fn: cls.get_schema(fn=fn) for fn in cls.fns(search=search, **kwargs)}

    # ASYNCIO LAND

    @classmethod
    def get_event_loop(self):
        import asyncio
        try:
            return asyncio.get_event_loop()
        except RuntimeError as e:
            return asyncio.new_event_loop()
    
    def new_event_loop(self):
        import asyncio
        return asyncio.new_event_loop()
    

    @classmethod
    def functions(cls,search:str=None,
                     include_parents:bool=True, 
                      include_hidden:bool = False) -> List[str]:
        '''
        Get a list of functions in a class
        
        Args;
            obj: the class to get the functions from
            include_parents: whether to include the parent functions
            include_hidden: whether to include hidden functions (starts and begins with "__")
        '''
        
        obj = cls
    
        functions = []
        parent_functions = [] 

        if include_parents:
            dir_list = dir(obj)
        else:
            # this only has atrributes for the child class
            dir_list = obj.__dict__.keys()

        for fn_name in dir_list:
            fn_obj = getattr(obj, fn_name)
            if not callable(fn_obj):
                continue
            
            # skip hidden functions if include_hidden is False
            if (include_hidden==False) and (fn_name.startswith('__') and fn_name.endswith('__')):
                
                continue
    
            # if the function is in the parent class, skip it
            if  (fn_name in parent_functions) and (include_parents==False):
                continue

            # if the function is a property, skip it
            if hasattr(type(obj), fn_name) and \
                isinstance(getattr(type(obj), fn_name), property):
                continue
            
            # if the function is callable, include it
            if callable(getattr(obj, fn_name)):
                functions.append(fn_name)
                            
        if search != None:
            functions = [f for f in functions if search in f]
            
        return functions
    
    fns = functions

    
    @classmethod
    def resolve_path(cls, path:str , extension:Optional[str]= None, root:bool = False):
        '''
        Resolves path for saving items that relate to the module
        
        The path is determined by the module path 
        
        '''
        
        if path.startswith('/'):
            path = path
        elif path.startswith('./'):
            path = os.path.abspath(path)
        else:
            # if it is a relative path, then it is relative to the module path
            # ex: 'data' -> '.commune/path_module/data'
            block_name = cls.block_name()
            tmp_dir = f'~/.{cls.library_name}/{block_name}'
            

            if tmp_dir not in path:
                path = os.path.join(tmp_dir, path)
            if not os.path.isdir(path):
                if extension != None and extension != path.split('.')[-1]:
                    path = path + '.' + extension
        if path.startswith('~/'):
            path =  os.path.expanduser(path)
        return path

    @classmethod
    def rm(cls, path:str):
        try:
            path = cls.resolve_path(path)
            os.remove(path)
            return {'success': True, 'path': path, 'msg': f'Removed {path}'}
        except Exception as e:
            return {'success': False, 'path': path, 'msg': f'Failed to remove {path}'}

    @classmethod
    def gather(cls,jobs:list, mode='asyncio', timeout:int = 20)-> list:
        
        import asyncio
        singleton = False

        if not isinstance(jobs, list):
            singleton = True
            jobs = [jobs]

        assert isinstance(jobs, list)

        if mode == 'asyncio':
            loop = a.get_event_loop()
            future = asyncio.wait_for(asyncio.gather(*jobs), timeout=timeout)
            results = loop.run_until_complete(future)
        else:
            raise NotImplementedError
        
        if singleton:
            return results[0]
        
        return results


    @classmethod
    def block_name(cls) -> str:
        import inspect
        # odd case where the module is a module in streamlit
        try:
            module_path =  inspect.getfile(cls)
        except Exception as e:
            if 'source code not available' in str(e):
                return cls.__name__
            else: 
                raise e
        return cls.path2name(module_path)
        return module_path
    
    name = block_name
    

    @classmethod
    def test(cls):
        test_fns = [fn for fn in cls.functions() if fn.startswith('test_')]
        for fn in test_fns:
            a.print(f'Running {fn}')
            getattr(cls, fn)()
        return {'status': 'success', 'msg': 'All tests passed.', 'tests': test_fns}

    @classmethod
    def sizeof(self, obj):
        import sys
        return sys.getsizeof(obj)
    @classmethod
    def time(self) -> float:
        import time
        return time.time()


    @classmethod
    def copy(cls, data: Any) -> Any:
        import copy
        return copy.deepcopy(data)
    
    @classmethod
    def round(cls, x:Union[float, int], sig: int=6, small_value: float=1.0e-9):
        import math
        """
        Rounds x to the number of {sig} digits
        :param x:
        :param sig: signifant digit
        :param small_value: smallest possible value
        :return:
        """
        x = float(x)
        return round(x, sig - int(math.floor(math.log10(max(abs(x), abs(small_value))))) - 1)
    
        
    @classmethod
    def serve(cls, tag:str=None, network:str=network, **kwargs):
        '''
        Serve a block
        '''
        return a.block('server')(block=cls(**kwargs), tag=tag, network=network)
    
    @classmethod
    def connect(cls, address, network=network, **kwargs):
        '''
        Connect to a block
        '''
        return a.block('server.client')(address=address, network=network, **kwargs)

    @classmethod
    def namespace(cls, network=network):
        return a.block('server.namespace').get_namespace(network=network)
    @classmethod
    def call(cls, address, fn, *args, network=network, timeout=10, **kwargs):
        '''
        Call a function in a block
        '''
        client = a.connect(address, network=network)
        return client.forward(fn=fn, args=args, kwargs=kwargs, timeout=timeout)
    

    # PORT LAND
    @classmethod
    def port_free(cls, *args, **kwargs) -> bool:
        return not cls.port_used(*args, **kwargs)

    @classmethod
    def port_available(cls, port:int, ip:str ='0.0.0.0'):
        return not cls.port_used(port=port, ip=ip)
        


    @classmethod
    def port_used(cls, port: int, ip: str = '0.0.0.0', timeout: int = 1):
        import socket
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Set the socket timeout
            sock.settimeout(timeout)

            # Try to connect to the specified IP and port
            try:
                sock.connect((ip, port))
                return True
            except socket.error:
                return False
            

    default_port_range = [50050, 50150]
    @classmethod
    def ports(cls):
        return cls.get('ports', list(range(*cls.default_port_range)) )
    
    @classmethod
    def set_ports(cls, start_port:int, end_port:int):
        assert end_port > start_port, f'End port must be greater than start port. {start_port} > {end_port}'

        ports = list(range(start_port, end_port))
        cls.put('ports', ports)
        return {'status': 'success', 'msg': f'Port range updated to {start_port} - {end_port}.'}
    

    @classmethod
    def used_ports(cls, ports:List[int] = None, ip:str = '0.0.0.0'):
        '''
        Get availabel ports out of port range
        
        Args:
            ports: list of ports
            ip: ip address
        
        '''
        if ports == None:
            ports = cls.ports()
        async def check_port(port, ip):
            return cls.port_used(port=port, ip=ip)
        jobs =  [check_port(port=port, ip=ip) for port in ports]
        results = cls.gather(jobs)
        used_ports = [port for port, result in zip(ports, results) if isinstance(result, bool) and result]
        return used_ports
    @classmethod
    def free_ports(cls, ports:List[int] = None, ip:str = '0.0.0.0'):
        ports = cls.ports()
        used_ports = cls.used_ports(ports=ports, ip=ip)
        free_ports = [port for port in ports if port not in used_ports]
        return free_ports
    
    @classmethod
    def free_port(cls, ip:str = '0.0.0.0'):
        return a.choice(cls.free_ports(ip=ip))
    @classmethod
    def free_address(cls,ip='0.0.0.0'):
        free_port = a.free_port(ip=ip)
        address = f'{ip}:{free_port}'
        return address
    
    @classmethod
    def resolve_address(cls, address:str = None) -> str:
        if address == None:
            address = a.free_address()
        assert isinstance(address, str), 'Address must be a string.'
        assert ':' in address, 'Address must be in the form ip:port'
        assert len(address.split(':')) == 2, 'Address must be in the form ip:port'
        ip, port = address.split(':')
        assert a.port_used(port=int(port), ip=ip) == False, f'Port {port} is already in use.'
        return address


    @classmethod
    def choice(cls, *args, **kwargs):
        import random
        return random.choice(*args, **kwargs)

    @classmethod
    def dict2str(cls, data:dict, indent:int = 4) -> str:
        import json
        return json.dumps(data, indent=indent)
    
    @classmethod
    def str2dict(cls, data:str) -> dict:
        import json
        return json.loads(data)

    @classmethod
    def tools(cls, search: str = None, info:bool = False) -> list:
        tools =  a.blocks('tool')
        if search != None:
            tools = [t for t in tools if t.startswith(search)]
        tools = sorted(tools)
        if info == True:
            tools = [a.block(t).info() for t in tools]
        return tools
    @classmethod
    def get_tool(cls, tool:str, return_fn=True, ):
        tool = a.block(tool)()

        from langchain.tools import Tool
        return Tool.from_function( func=tool.call, 
                                  name=tool.name(),
                                  description="useful for when you need to answer questions about current events"),

    @classmethod
    def tool2info(cls, return_json_str:bool = False):
        import json
        tool2info= {}
        for tool in a.tools(info=False):
            tool_info = a.block(tool).info()
            tool2info[tool] = tool_info
            if return_json_str:
                print(tool_info['schema']['input'])
                tool2info[tool] = json.dumps(tool_info, indent=4)

        cls.put_json('./tool2info.json', tool2info)
        return tool2info
    
    @classmethod
    def tool2vec(cls, batch_size:int = 10):
        model = a.block('llm.openai')()
        tool2info = cls.tool2info(return_json_str=True)
        tools = list(tool2info.keys())
        infos = list(tool2info.values())

        tool2vec = {}
        for i in range(0, len(tools), batch_size):
            print(f'Generating vectors for {i} - {i+batch_size} out of {len(tools)}')
            batch_tools = tools[i:i+batch_size]
            batch_infos = infos[i:i+batch_size]
            vectors = model.embed(input=batch_infos)
            for tool, vector in zip(batch_tools, vectors):
                tool2vec[tool]  = vector

        cls.put_json('./tool2vec.json', tool2vec)

     
    

Block = a

