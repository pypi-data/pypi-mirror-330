# ---- render code block -----
from databloom._core.dataset import DatasetBase
from .table import *

class hainv42(DatasetBase):
    def __init__(self) -> None:
        self.database_id = "67c4553800b78c7a79e58b88"
        self.database_name  = "hainv42"
        
        self.testable2 = testable2(self.database_name)
        
# ---- render code block 
    
