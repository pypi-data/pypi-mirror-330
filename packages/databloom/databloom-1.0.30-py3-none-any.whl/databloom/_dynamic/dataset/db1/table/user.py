# ---- render code block -----
from databloom._core.dataset.table_core import TableBase

class user(TableBase):
    def __init__(self, db_name: str) -> None:
        self.table_name = "user"
        self.set_db_name(db_name)
# ---- render code block -----