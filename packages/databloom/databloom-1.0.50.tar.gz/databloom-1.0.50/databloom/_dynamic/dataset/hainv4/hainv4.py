# ---- render code block -----
from databloom._core.dataset import DatasetBase
from .table import *

class hainv4(DatasetBase):
    def __init__(self) -> None:
        self.database_id = "67c44bf100b78c7a79e58b86"
        self.database_name  = "hainv4"
        
        self.testable = testable(self.database_name)
        
# ---- render code block 
    
