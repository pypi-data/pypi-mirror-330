# --- render code block -----
from databloom._core.postgres_core import PostgresqlBase

class bumdata(PostgresqlBase):
    def __init__(self, get_credential_from_server) -> None:
        self.id = "67b9a978f83cc8e6de004775"
        self.credential = get_credential_from_server(self.id)
# --- render code block -----
