
import warnings
warnings.filterwarnings("ignore")
import autonomy as a

class CLI(a.Block):
    """
    Create and init the CLI class, which handles the coldkey, hotkey and tao transfer 
    """
    # 
    def __init__(
            self, 
            *args,
            **kwargs
        ) :
        self.block = a.Block()


        args, kwargs = self.parse_args()
    
        blocks = a.blocks()

        fn = None
        block = None
        # is it a fucntion, assume it is for the module
        
        
        # RESOLVE THE MODULE
        blocks = a.blocks()
        if args[0] in blocks:
            # is a module
            block = args.pop(0)
            block  = a.block(block)
        
        else:
            # is a function
            block = a.Block

        assert len(args) > 0, 'No function or module specified'
        fn = args.pop(0)  
        if block.is_self_method(fn):
            fn = getattr(block(), fn)
        else:
            fn = getattr(block, fn)
        if callable(fn):
            result = fn(*args, **kwargs)
        a.print(result)


    @classmethod
    def parse_args(cls, argv = None):
        if argv is None:
            argv = cls.argv()

        args = []
        kwargs = {}
        parsing_kwargs = False
        for arg in argv:
            # TODO fix exception with  "="
            # if any([arg.startswith(_) for _ in ['"', "'"]]):
            #     assert parsing_kwargs is False, 'Cannot mix positional and keyword arguments'
            #     args.append(cls.determine_type(arg))
            if '=' in arg:
                parsing_kwargs = True
                key, value = arg.split('=', 1)
                # use determine_type to convert the value to its actual type
                
                kwargs[key] = cls.determine_type(value)
            else:
                assert parsing_kwargs is False, 'Cannot mix positional and keyword arguments'
                args.append(cls.determine_type(arg))
        return args, kwargs
    


    @classmethod
    def determine_type(cls, x):
        if x.lower() == 'null' or x == 'None':
            return None
        elif x.lower() in ['true', 'false']:
            return bool(x.lower() == 'true')
        elif x.startswith('[') and x.endswith(']'):
            # this is a list
            try:
                
                list_items = x[1:-1].split(',')
                # try to convert each item to its actual type
                x =  [cls.determine_type(item.strip()) for item in list_items]
                if len(x) == 1 and x[0] == '':
                    x = []
                return x
       
            except:
                # if conversion fails, return as string
                return x
        elif x.startswith('{') and x.endswith('}'):
            # this is a dictionary
            if len(x) == 2:
                return {}
            try:
                dict_items = x[1:-1].split(',')
                # try to convert each item to a key-value pair
                return {key.strip(): cls.determine_type(value.strip()) for key, value in [item.split(':', 1) for item in dict_items]}
            except:
                # if conversion fails, return as string
                return x
        else:
            # try to convert to int or float, otherwise return as string
            try:
                return int(x)
            except ValueError:
                try:
                    return float(x)
                except ValueError:
                    return x


    @classmethod
    def argv(cls, include_script:bool = False):
        import sys
        args = sys.argv
        if include_script:
            return args
        else:
            return args[1:]