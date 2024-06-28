""" Container """
from typing import Any, Callable, Self
from functools import partial

################################################################################

class Singleton (type):
    _instances: dict = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        # else:
            # cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]

class Container(metaclass=Singleton):
    
    _container: dict[str, tuple[Callable, dict[str, Any]]] = {}
    
    def __getiitem__(self, key: str):
        return self._container[key]
    
    def __contains__(self, key):
        return key in self._container
    
    def inject(self, key: str, get_dep: Callable, **configs)->None:
        """"""
        if key in self._container:
            raise Exception()
        
        self._container[key] = (get_dep, configs)
    
    def provide(self, key: str)->tuple[Callable, dict]:
        """"""
        if key not in self._container:
            raise Exception()

        return self._container[key]

def inject_dependency(key: str, get_dep: Callable, **configs)->None:
    """"""
    container = Container()
    container.inject(key, get_dep, **configs)

def provide_dependency(key: str, **override_configs)->Callable:
    """"""
    container = Container()
    get_dep, configs = container.provide(key)
    merged_config = {**configs, **override_configs}
    return partial(get_dep, **merged_config)


if __name__ == '__main__':
    
    def get_dep1(name: str, url:str, level:int):
        return f'{name}/{url}/{level}'
    
    inject_dependency('dep1', get_dep= get_dep1, name='RBELLI', url='cahier.com', level=10)
    
    depa = provide_dependency('dep1')
    print(depa())
    
    depb = provide_dependency('dep1', name='NAMe2', url='NEWURL.com', level=45)
    print(depb())
    
    try:
        depc = provide_dependency('dep1', NOKEY='NAMe2', url='NEWURL.com', level=45)
        print(depc())
    except Exception as e:
        print(e)