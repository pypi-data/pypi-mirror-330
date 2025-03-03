# ---- render code block -----
from databloom._core.dataset.table_core import TableBase

class test2(TableBase):
    """
    Table created for pipeline destination
    """
    def __init__(self, db_name: str) -> None:
        self.table_id = "d68c0157-6e8e-433b-b0c6-7fa37b58864b"
        self.table_name = "test2"
        self.set_db_name(db_name)
# ---- render code block -----
