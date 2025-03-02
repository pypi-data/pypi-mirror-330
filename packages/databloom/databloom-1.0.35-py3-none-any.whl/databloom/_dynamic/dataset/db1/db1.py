from databloom._core.dataset import DatasetBase
from .table.user import user
from .table.credit import credit

class db1(DatasetBase):
    def __init__(self) -> None:
        # ---- render code block
        self.database_name  = "db1"
        self.user = user(self.database_name)
        self.credit = credit(self.database_name)
        # ---- render code block 
    