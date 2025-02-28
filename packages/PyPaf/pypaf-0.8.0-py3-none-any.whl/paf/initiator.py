"""Initiator Decorator"""

import functools

def attribute_init(func):
    """Decorator to initiate an object based on a list of attributes"""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        """Initiate properties from specified dict"""
        for key in list(getattr(self, 'attrs', [])):
            object.__setattr__(self, key, '')
        if kwargs:
            elements = kwargs
        else:
            elements = args[0]
        for key, val in elements.items():
            if hasattr(self, key):
                object.__setattr__(self, key, str(val))
        return func(self, *args, **kwargs)

    return wrapper
