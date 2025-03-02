import databloom._dynamic.dataset as ds
from typing import Callable

class Dataset:
    """
    data source type is mysql
    """
    def __init__(self) -> None:
        ## ----render code block-----
        self.db1 = ds.db1()
        self.unity = ds.unity()
        ## ----render code block----
        pass


