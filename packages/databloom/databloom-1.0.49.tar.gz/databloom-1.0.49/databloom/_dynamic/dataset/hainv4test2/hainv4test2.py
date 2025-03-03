# ---- render code block -----
from databloom._core.dataset import DatasetBase
from .table import *

class hainv4test2(DatasetBase):
    def __init__(self) -> None:
        self.database_id = "67c4815d83416b9075d83eac"
        self.database_name  = "hainv4test2"
        
        self.test2 = test2(self.database_name)
        
# ---- render code block 
    
