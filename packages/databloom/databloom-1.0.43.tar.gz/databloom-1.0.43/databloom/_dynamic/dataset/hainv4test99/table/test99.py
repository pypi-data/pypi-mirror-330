# ---- render code block -----
from databloom._core.dataset.table_core import TableBase

class test99(TableBase):
    """
    Table created for pipeline destination
    """
    def __init__(self, db_name: str) -> None:
        self.table_id = "a1b351a9-8401-4463-bddd-65c3ad656f93"
        self.table_name = "test99"
        self.set_db_name(db_name)
# ---- render code block -----
