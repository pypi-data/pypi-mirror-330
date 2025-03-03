import inspect

from typing import Any

class KwargsMeta(type):
    def __new__(cls, name: str, bases: tuple, dct: dict[str, Any]) -> Any:
        # Extract kwargs from all methods
        kwargs_defaults = set()
        for attr_name, attr_value in dct.items():
            # ignore __init__ method and only check for methods
            if callable(attr_value) and not attr_name.startswith('_'):

                # Extract kwargs from the signature
                sig = inspect.signature(attr_value)
                for param in sig.parameters.values():
                    if param.default != inspect.Parameter.empty:
                        kwargs_defaults.add(param.name)

        # Modify the __init__ method to accept kwargs
        def get_init(original_init):
            # Update signature
            init_signature = inspect.signature(original_init)
            new_params = list(init_signature.parameters.values())

            # Add default kwargs to the signature
            for key in kwargs_defaults:
                if key not in init_signature.parameters.keys():
                    new_params.append(inspect.Parameter(key, inspect.Parameter.KEYWORD_ONLY, default = None))

            # Create new signature
            new_signature = init_signature.replace(parameters = new_params)
            orig_kwarg_names = init_signature.parameters.keys()

            # Create new __init__ method
            def __init__(self, *args, **kwargs):
                for key in kwargs_defaults:
                    setattr(self, key, kwargs.get(key))
                
                # Call the original __init__ method with the original kwargs
                orig_kwargs = {key: value for key, value in kwargs.items() if key in orig_kwarg_names}
                original_init(self, *args, **orig_kwargs)
        
            __init__.__signature__ = new_signature
            return __init__
        
        # Replace the __init__ method with the new one
        original_init = dct.get('__init__', lambda self: None)
        dct['__init__'] = get_init(original_init)

        # Update methods to use default kwargs
        for attr_name, attr_value in dct.items():
            # Ignore __init__ method and only check for methods
            if callable(attr_value) and not attr_name.startswith('_'):

                # Create a wrapper for the method
                def wrapper(func):
                    
                    # Extract kwargs from the signature
                    func_signature = inspect.signature(func)
                    func_kwargs = set()
                    for param in func_signature.parameters.values():
                        if param.default != inspect.Parameter.empty:
                            func_kwargs.add(param.name)

                    # Create a new method that uses default kwargs
                    def new_func(self, *args, **kwargs):
                        # Bind the arguments to the function
                        bound_kwargs = func_signature.bind(self, *args, **kwargs)
                        for key in func_kwargs:
                            # If the key is not in the kwargs, but is in the class, use the class attribute
                            if key not in kwargs:
                                if getattr(self, key, None) is not None:
                                    bound_kwargs.arguments[key] = getattr(self, key)
                        
                        # Apply the default values
                        bound_kwargs.apply_defaults()
                        return func(*bound_kwargs.args, **bound_kwargs.kwargs)
                    
                    # Update the signature of the new method
                    parameters = [
                        param.replace(default = None) if param.name in func_kwargs else param 
                        for param in func_signature.parameters.values()
                    ]

                    # Create a new signature
                    new_signature = func_signature.replace(parameters = parameters)
                    new_func.__signature__ = new_signature

                    # Set the name of the new function to the original name
                    new_func.__name__ = func.__name__
                
                    return new_func
                
                # Replace the method with the new one
                dct[attr_name] = wrapper(attr_value)
            
        return super().__new__(cls, name, bases, dct)

