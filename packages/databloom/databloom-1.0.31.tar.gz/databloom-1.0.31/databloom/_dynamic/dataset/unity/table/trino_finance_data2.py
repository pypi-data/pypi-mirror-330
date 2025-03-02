# ---- render code block -----
from databloom._core.dataset.table_core import TableBase

class trino_finance_data2(TableBase):
    def __init__(self, db_name: str) -> None:
        self.table_name = "trino_finance_data2"
        self.set_db_name(db_name)
# ---- render code block -----