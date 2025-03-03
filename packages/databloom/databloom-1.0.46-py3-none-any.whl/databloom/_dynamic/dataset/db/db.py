# ---- render code block -----
from databloom._core.dataset import DatasetBase
from .table import *

class db(DatasetBase):
    def __init__(self) -> None:
        self.database_id = "67bfdf44fa60f7ca645ddc7c"
        self.database_name  = "db"
        
        self.new_table_name = new_table_name(self.database_name)
        
# ---- render code block 
    
