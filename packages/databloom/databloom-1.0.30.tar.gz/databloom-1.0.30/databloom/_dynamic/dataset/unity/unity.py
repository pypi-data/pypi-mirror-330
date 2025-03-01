# ---- render code block -----
from databloom._core.dataset import DatasetBase
from .table.trino_finance_data2 import trino_finance_data2
from .table.hainv4_campaign_2 import hainv4_campaign_2
class unity(DatasetBase):
    def __init__(self) -> None:       
        self.database_name  = "unity"
        self.trino_finance_data2 = trino_finance_data2(self.database_name)
        self.hainv4_campaign_2 = hainv4_campaign_2(self.database_name)
# ---- render code block 
    