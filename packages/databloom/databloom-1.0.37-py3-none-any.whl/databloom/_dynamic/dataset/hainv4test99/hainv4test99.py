# ---- render code block -----
from databloom._core.dataset import DatasetBase
from .table import *

class hainv4test99(DatasetBase):
    def __init__(self) -> None:
        self.database_id = "67c3543fa83a0276c0a76865"
        self.database_name  = "hainv4test99"
        
        self.test99 = test99(self.database_name)
        
# ---- render code block 
    
