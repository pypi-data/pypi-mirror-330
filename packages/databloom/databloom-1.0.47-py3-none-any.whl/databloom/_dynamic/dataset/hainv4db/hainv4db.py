# ---- render code block -----
from databloom._core.dataset import DatasetBase
from .table import *

class hainv4db(DatasetBase):
    def __init__(self) -> None:
        self.database_id = "67c344a7a83a0276c0a76861"
        self.database_name  = "hainv4db"
        
        self.table_hoang_test = table_hoang_test(self.database_name)
        
# ---- render code block 
    
