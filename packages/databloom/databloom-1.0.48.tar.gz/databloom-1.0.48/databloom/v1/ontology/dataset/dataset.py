import databloom._dynamic.dataset as ds
from typing import Callable

class Dataset:
    """
    data source type is mysql
    """
    def __init__(self) -> None:
        ## ----render code block-----
        
        self.db = ds.db()
        self.hainv4db = ds.hainv4db()
        self.hainv4test99 = ds.hainv4test99()
        self.hoangtestdb = ds.hoangtestdb()
        self.unity = ds.unity()
        self.unity2 = ds.unity2()
        self.hainv4 = ds.hainv4()
        self.hainv42 = ds.hainv42()
        ## ----render code block----
        pass
