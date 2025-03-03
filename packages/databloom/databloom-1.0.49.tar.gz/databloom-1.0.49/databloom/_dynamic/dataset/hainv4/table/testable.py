# ---- render code block -----
from databloom._core.dataset.table_core import TableBase

class testable(TableBase):
    """
    Table created for pipeline destination
    """
    def __init__(self, db_name: str) -> None:
        self.table_id = "9e153e4f-ed75-4118-a59c-2c5980c30d28"
        self.table_name = "testable"
        self.set_db_name(db_name)
# ---- render code block -----
