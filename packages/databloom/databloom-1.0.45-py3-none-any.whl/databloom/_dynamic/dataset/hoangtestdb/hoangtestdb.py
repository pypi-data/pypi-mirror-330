# ---- render code block -----
from databloom._core.dataset import DatasetBase
from .table import *

class hoangtestdb(DatasetBase):
    def __init__(self) -> None:
        self.database_id = "67c3e537ead024e27fea7f58"
        self.database_name  = "hoangtestdb"
        
        self.abc = abc(self.database_name)
        
# ---- render code block 
    
