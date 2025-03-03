# ---- render code block -----
from databloom._core.dataset import DatasetBase
from .table import *

class unity(DatasetBase):
    def __init__(self) -> None:
        self.database_id = "67c41b79ead024e27fea7f5b"
        self.database_name  = "unity"
        
        self.hainv4campaign = hainv4campaign(self.database_name)
        
# ---- render code block 
    
